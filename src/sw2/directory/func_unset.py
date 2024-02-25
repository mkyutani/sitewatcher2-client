import sys
from sw2.directory.list import get_directories
from sw2.directory.unset import unset_directory_variables
from sw2.util import is_uuid

def sw2_parser_directory_unset(subparser):
    parser = subparser.add_parser('unset', help='unset metadata of directory')
    parser.add_argument('id', help='directory id or name')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_unset(args):
    args_id = args.get('id')
    args_key = args.get('key')
    args_strict = args.get('strict')

    if is_uuid(args_id):
        ids = [args_id]
    else:
        directories = get_directories(args_id, strict=args_strict)
        if len(directories) == 0:
            print('directory not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in directories]

    ids.sort()

    for id in ids:
        unset_directory_variables(id, args_key)

    return 0