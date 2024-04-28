import json
import sys
from sw2.directory.list import list_directories
from sw2.directory.variables import get_directory_variables
from sw2.util import is_uuid

def sw2_parser_directory_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_variables(args):
    args_name = args.get('name')
    args_key = args.get('key')
    args_json = args.get('json')
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

    all_metadata = []
    for id in ids:
        metadata = get_directory_variables(id, args_key)
        if metadata is None:
            return 1

        all_metadata.extend(metadata)

    if args_json:
        print(json.dumps(all_metadata))
    else:
        for m in all_metadata:
            message = ' '.join([m['directory'], m['directory_name'], m['key'], m['value']])
            print(message)

    return 0