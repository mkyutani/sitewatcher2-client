import sys

from sw2.channel.delete import delete_channel
from sw2.channel.list import get_channels
from sw2.util import is_uuid

def sw2_parser_channel_delete(subparser):
    parser = subparser.add_parser('delete', help='add channel')
    parser.add_argument('name', help='channel id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='channel name strict mode')
    return []

def sw2_channel_delete(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        ids = [args_name]
    else:
        channels = get_channels(args_name, strict=args_strict)
        if channels is None:
            return 1
        elif len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in channels]

    failures = 0
    for id in ids:
        result = delete_channel(id)
        if result is False:
            print('failed to delete {id}', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0