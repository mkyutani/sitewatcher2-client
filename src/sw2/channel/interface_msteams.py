import re
import sys
import time
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError, SlackApiError

from sw2.formatter import PrivateFormatter


def send_to_msteams(device_info, channel_resources, sending=False):
    msteams_webhook = device_info['apikey']
    msteams_title = device_info['tag']
    msteams_template = eval('"' + device_info['template'] + '"') # convert raw string to string

    if not msteams_title:
        msteams_title = 'sitewatcher2'

    all_resource_list = []
    resource_list = []
    count = 0
    for channel_resource in channel_resources:
        formatter = PrivateFormatter()
        for kv in channel_resource['kv']:
            formatter.set(kv['key'], kv['value'])
        item = formatter.format(msteams_template)
        resource_list.append(f'- {item}\r')
        count = count + 1
        if count > 10:
            all_resource_list.append(resource_list)
            resource_list = []
            count = 0
    if len(resource_list) > 0:
        all_resource_list.append(resource_list)

    initial = True
    for resource_list in all_resource_list:
        if not initial and sending:
            time.sleep(5)
        else:
            initial = False

        text = ''.join(resource_list)
        text_crlf_removed = re.sub(r'[\r\n]', ' ', text)
        contents = [
            {
                'text': text
            }
        ]

        data = {
            'type': 'message',
            'attachments': [
                {
                    'contentType': 'application/vnd.microsoft.teams.card.o365connector',
                    'content': {
                        '@type': 'MessageCard',
                        '@context': 'https://schema.org/extensions',
                        'title': msteams_title,
                        'sections': contents
                    }
                }
            ]
        }

        res = None
        try:
            verb = 'Sending'
            if sending:
                res = requests.post(msteams_webhook, json=data)
                if res is None:
                    print(f'None {text_crlf_removed}', file=sys.stderr)
                    continue
                elif res.status_code >= 400:
                    print(f'{res.status_code} {text_crlf_removed}', file=sys.stderr)
                    continue
                verb = res.status_code
            print(f'{verb} {msteams_title} {text_crlf_removed}', file=sys.stderr)
        except Exception as e:
            print(f'{type(e).__name__} {text_crlf_removed}', file=sys.stderr)
            print(e, file=sys.stderr)

    return 0