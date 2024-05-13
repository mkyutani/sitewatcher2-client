import json
import sys

from sw2.channel.list import get_channels

def sw2_parser_channel_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--sites', action='store_true', help='list sites')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_channel_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_sites = args.get('sites')
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
            if args_sites:
                for directory in channel['directories']:
                    print(' ', str(directory['id']), directory['name'], sep=args_delimiter)
                for site in channel['sites']:
                    print(' ', str(site['id']), site['name'], sep=args_delimiter)

    return 0