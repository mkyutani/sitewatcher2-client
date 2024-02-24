import json
import sys
from urllib.parse import urljoin
import requests
from sw2.directory.list import get_directories
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_directory_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of directory')
    parser.add_argument('id', help='directory id or name')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def get_directory_variables(id, key=None, strict=False):
    headers = { 'Cache-Control': 'no-cache' }

    if key is not None:
        key_path = f'?key={key}'
    else:
        key_path = ''

    query = urljoin(Environment().apiDirectories(), f'{id}/metadata{key_path}')

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    metadata = json.loads(res.text)

    return metadata

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