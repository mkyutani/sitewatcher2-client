import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channels
from sw2.site.list import get_sites

def sw2_parser_channel_add_device(subparser):
    parser = subparser.add_parser('add-device', help='add channel device')
    parser.add_argument('channel', help='channel')
    parser.add_argument('device', help='device name')
    parser.add_argument('interface', help='interface name')
    parser.add_argument('header', help='header template')
    parser.add_argument('body', help='body template')
    parser.add_argument('--strict', action='store_true', help='strict mode')
    return []

def sw2_channel_add_device(args):
    args_channel = args.get('channel')
    args_device = args.get('device')
    args_interface = args.get('interface')
    args_header = args.get('header')
    args_body = args.get('body')
    args_strict = args.get('strict')

    if is_uuid(args_channel):
        channel_id = args_channel
    else:
        channels = get_channels(args_channel, strict=args_strict)
        if channels is None:
            return 1
        elif len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return 1
        elif len(channels) > 1:
            print('only one channel allowed', file=sys.stderr)
            return 1

        channel_id = channels[0]['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'interface': args_interface,
        'header': args_header,
        'body': args_body
    }

    res = None
    try:
        res = requests.post(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'devices', args_device])), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel_device_pair = json.loads(res.text)
    print(str(channel_device_pair['channel']), str(channel_device_pair['device']))

    return 0