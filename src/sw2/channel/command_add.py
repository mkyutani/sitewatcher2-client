import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_channel_add(subparser):
    parser = subparser.add_parser('add', aliases=['a'], help='add channel')
    parser.add_argument('name', metavar='NAME', help='name')

def sw2_channel_add(args):
    args_name = args.get('name')

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
    }

    res = None
    try:
        res = requests.post(Environment().apiChannels(), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel = json.loads(res.text)
    print(str(channel['id']))

    return 0