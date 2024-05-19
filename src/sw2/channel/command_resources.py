import json
import requests
import sys
from urllib.parse import urljoin

from sw2.channel.list import get_channels
from sw2.env import Environment

def sw2_parser_channel_resources(subparser):
    parser = subparser.add_parser('resources', help='get resources of channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def sw2_channel_resources(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    for channel in channels:
        headers = {}

        res = None
        try:
            res = requests.get(urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'resources'])), headers=headers)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        if args_json:
            print(res.text)
        else:
            channel_resources = json.loads(res.text)
            for channel_resource in channel_resources:
                print(channel_resource['channel'])
                for kv in channel_resource['kv']:
                    print('-', kv['key'], kv['value'], sep=args_delimiter)

    return 0