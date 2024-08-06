import re
import string
import time
import requests
import sys
from urllib.parse import urljoin

from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError, SlackApiError

def create_message(template, channel_resource):
    class SilentFormatter(string.Formatter):
        def get_value(self, key, *args, **kwargs):
            if not key in args[1]:
                return '*'
            else:
                return super().get_value(key, *args, **kwargs)

    class Vars:
        def __init__(self):
            pass
        def s(self, k, v):
            setattr(self, k, v)
        def g(self, k):
            return getattr(self, k)
        def m(self, t):
            f = SilentFormatter()
            return f.format(t, **self.__dict__)

    vars = Vars()
    for kv in channel_resource['kv']:
        vars.s(kv['key'], kv['value'])
    return vars.m(template)

def output_to_device(device_info, channel_resources, sending=False):
    if device_info['interface'] == 'slack':
        slack_api_key = device_info['apikey']
        slack_channel = device_info['tag']
        slack_template = eval('"' + device_info['template'] + '"') # convert raw string to string

        client = WebClient(token=slack_api_key)
        channel = '#' + slack_channel

        for channel_resource in channel_resources:
            try:
                slack_message =  create_message(slack_template, channel_resource)
                verb = 'Sending'
                if sending:
                    client.chat_postMessage(channel=channel, text=slack_message)
                    verb = 'Sent'
                slack_message_crlf_removed = re.sub(r'[\r\n]', ' ', slack_message)
                print(f'{verb} to {channel}: {slack_message_crlf_removed}', file=sys.stderr)
            except SlackApiError as e:
                if e.response.status_code == 429:
                    delay = int(e.response.headers['Retry-After'])
                    print('Rate limited. Retrying in {} seconds'.format(delay), file=sys.stderr)
                    time.sleep(delay)
                    client.chat_postMessage(channel=channel, text=slack_message)
                elif e.response.status_code < 400:
                    print('Slack api error: Status={}, Reason={}'.format(e.response.status_code, e.response['error']), file=sys.stderr)
            except SlackClientError as e:
                print(e)

    return 0