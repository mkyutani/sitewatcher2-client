import sys
from sw2.directory.list import list_directories
from sw2.directory.unset import unset_directory_variables
from sw2.util import is_uuid

def sw2_parser_directory_unset(subparser):
    parser = subparser.add_parser('unset', help='unset metadata of directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')
    return []

def sw2_directory_unset(args):
    args_name = args.get('name')
    args_key = args.get('key')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        ids = [args_name]
    else:
        directories = list_directories(args_name, strict=args_strict)
        if directories is None:
            return 1
        elif len(directories) == 0:
            print('directory not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in directories]

    ids.sort()

    for id in ids:
        unset_directory_variables(id, args_key)

    return 0