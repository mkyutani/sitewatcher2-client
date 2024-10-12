import re
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError, SlackApiError

from sw2.formatter import PrivateFormatter

def send_to_slack(device_info, channel_resources, sending=False):
    slack_api_key = device_info['apikey']
    slack_channel = device_info['tag']
    slack_template = eval('"' + device_info['template'] + '"') # convert raw string to string

    client = WebClient(token=slack_api_key)
    channel = '#' + slack_channel

    for channel_resource in channel_resources:
        try:
            formatter = PrivateFormatter()
            for kv in channel_resource['kv']:
                key = kv['key']
                value_string = eval('"' + kv['value'] + '"') # convert raw string to string
                formatter.set(key, value_string)
            slack_message = formatter.format(slack_template)
            verb = 'Sending'
            if sending:
                client.chat_postMessage(channel=channel, text=slack_message)
                verb = 'Sent'
            slack_message_crlf_removed = re.sub(r'[\r\n]', ' ', slack_message)
            print(f'{verb} to {channel}: {slack_message_crlf_removed}', file=sys.stderr)
        except SlackApiError as e:
            if e.response.status_code == 429:
                delay = int(e.response.headers['Retry-After'])
                print(f'Rate limited. Retrying in {delay} seconds: {slack_message_crlf_removed}', file=sys.stderr)
                time.sleep(delay)
                client.chat_postMessage(channel=channel, text=slack_message)
                print(f'{verb} to {channel}: {slack_message_crlf_removed}', file=sys.stderr)
            elif e.response.status_code < 400:
                print('Slack api error: Status={}, Reason={}'.format(e.response.status_code, e.response['error']), file=sys.stderr)
        except SlackClientError as e:
            print(e)

    return 0