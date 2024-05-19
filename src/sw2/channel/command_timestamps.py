import json
import requests
import sys
from urllib.parse import urljoin

from sw2.channel.list import get_channels
from sw2.env import Environment

def sw2_parser_channel_timestamps(subparser):
    parser = subparser.add_parser('timestamps', help='get timestamps when resources has been collected')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def sw2_channel_timestamps(args):
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
            res = requests.get(urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'timestamps'])), headers=headers)
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
            channel_timestamps = json.loads(res.text)
            print(channel['id'], channel['name'], sep=args_delimiter)
            for timestamp in channel_timestamps['timestamps']:
                print('-', timestamp['timestamp'], sep=args_delimiter)

    return 0