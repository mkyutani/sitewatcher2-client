import json
import sys
from sw2.directory.list import get_directories
from sw2.directory.set import set_directory_variables
from sw2.util import is_uuid

def sw2_parser_directory_set(subparser):
    parser = subparser.add_parser('set', help='set metadata of directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('key', default=None, help='metadata key')
    parser.add_argument('value', default=None, help='metadata value')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_set(args):
    args_name = args.get('name')
    args_key = args.get('key')
    args_value = args.get('value') if args.get('value') else ''
    args_json = args.get('json')
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

    ids.sort()

    for id in ids:
        metadata = set_directory_variables(id, args_key, args_value)
        if metadata is not None:
            metadata.sort(key=lambda x: x['key'])
            if args_json:
                print(json.dumps(metadata))
            else:
                for m in metadata:
                    message = ' '.join([m['directory'], m['key'], m['value']])
                    print(message)

    return 0