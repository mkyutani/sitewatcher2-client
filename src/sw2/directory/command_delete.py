import sys

from sw2.directory.delete import delete_directory
from sw2.directory.list import get_directories
from sw2.util import is_uuid

def sw2_parser_directory_delete(subparser):
    parser = subparser.add_parser('delete', help='add directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')
    return []

def sw2_directory_delete(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        ids = [args_name]
    else:
        directories = get_directories(args_name, strict=args_strict)
        if directories is None:
            return 1
        elif len(directories) == 0:
            print('directory not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in directories]

    failures = 0
    for id in ids:
        result = delete_directory(id)
        if result is False:
            print(f'failed to delete {id}', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0