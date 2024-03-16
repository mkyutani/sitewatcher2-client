import sys

from sw2.directory.list import get_directories
from sw2.directory.rename import rename_directory
from sw2.util import is_uuid

def sw2_parser_directory_rename(subparser):
    parser = subparser.add_parser('rename', help='rename directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('new', help='new name')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_rename(args):
    args_name = args.get('name')
    args_new = args.get('new')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        id = args_name
    else:
        directory = get_directories(args_name, strict=args_strict, single=True)
        if directory is None:
            return 1

        id = directory['id']

    result = rename_directory(id, args_new)
    if result is False:
        print('failed to rename {id}', file=sys.stderr)
        return 1
    else:
        return 0