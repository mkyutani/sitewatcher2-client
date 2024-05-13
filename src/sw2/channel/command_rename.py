import sys

from sw2.channel.list import get_channels
from sw2.channel.rename import rename_channel
from sw2.util import is_uuid

def sw2_parser_channel_rename(subparser):
    parser = subparser.add_parser('rename', help='rename channel')
    parser.add_argument('name', help='channel id, name or "all"')
    parser.add_argument('new', help='new name')
    parser.add_argument('--strict', action='store_true', help='channel name strict mode')
    return []

def sw2_channel_rename(args):
    args_name = args.get('name')
    args_new = args.get('new')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        id = args_name
    else:
        channels = get_channels(args_name, strict=args_strict)
        if channels is None:
            return 1

        if len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return 1
        elif len(channels) > 1:
            print('multiple channels found', file=sys.stderr)
            return 1

        id = channels[0]['id']

    result = rename_channel(id, args_new)
    if result is False:
        print('failed to rename {id}', file=sys.stderr)
        return 1
    else:
        return 0