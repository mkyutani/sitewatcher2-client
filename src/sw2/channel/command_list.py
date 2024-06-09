import json
import sys

from sw2.channel.list import get_channels

def sw2_parser_channel_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--compact', action='store_true', help='in compact format')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_channel_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_compact = args.get('compact')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    channels.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(channels))
    else:
        for channel in channels:
            print(str(channel['id']), channel['name'], sep=args_delimiter)
            if not args_compact:
                for directory in channel['directories']:
                    print(f'- directory {str(directory["id"])} {directory["name"]}')
                for site in channel['sites']:
                    print(f'- site {str(site["id"])} {site["name"]}')
                for device in channel['devices']:
                    print(f'- device {device["name"]} {device["interface"]}')
                for timestamp in channel['timestamps']:
                    print(f'- timestamp {timestamp["timestamp"]}')

    return 0