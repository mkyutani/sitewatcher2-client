import json
import sys
from sw2.directory.list import get_directories
from sw2.directory.variables import get_directory_variables
from sw2.util import is_uuid

def sw2_parser_directory_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of directory')
    parser.add_argument('id', help='directory id or name')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_variables(args):
    args_id = args.get('id')
    args_key = args.get('key')
    args_json = args.get('json')
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
        metadata = get_directory_variables(id, args_key)
        if metadata is None:
            return 1

        if args_json:
            print(json.dumps(metadata))
        else:
            for m in metadata:
                message = ' '.join([m['directory'], m['key'], m['value']])
                print(message)

    return 0