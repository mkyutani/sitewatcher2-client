import sys

from sw2.directory.enable import enable_directories
from sw2.directory.list import get_directories
from sw2.util import is_uuid

def sw2_parser_directory_enable(subparser):
    parser = subparser.add_parser('enable', help='enable directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_enable(args):
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
        result = enable_directories(id)
        if result is False:
            print('failed to enable {id}', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0