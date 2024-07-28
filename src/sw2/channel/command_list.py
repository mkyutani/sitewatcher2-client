import json
import sys

import yaml

from sw2.channel.list import get_channels

def sw2_parser_channel_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('--detail', action='store_true', help='show detail')
    format_group.add_argument('--json', action='store_true', help='in json format')
    format_group.add_argument('--yaml', action='store_true', help='in yaml format')
    return aliases

def sw2_channel_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_yaml = args.get('yaml')

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    channels.sort(key=lambda x: x['id'])

    if args_json:
        json.dump(channels, sys.stdout)
    elif args_yaml:
        yaml.dump(channels, sys.stdout)
    else:
        for channel in channels:
            print(f'channel {channel["id"]} {channel["name"]}')
            if args_detail:
                for directory in channel['directories']:
                    print(f'- directory {directory["id"]} {directory["name"]}')
                for site in channel['sites']:
                    print(f'- site {site["id"]} {site["name"]}')
                for device in channel['devices']:
                    print(f'- device {device["name"]} {device["interface"]} {device["tag"]}')
                for timestamp in channel['timestamps']:
                    print(f'- timestamp {timestamp["timestamp"]}')
    return 0