import json
import sys
from urllib.parse import urljoin
import requests
from sw2.directory.list import get_directories
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_directory_unset(subparser):
    parser = subparser.add_parser('unset', help='unset metadata of directory')
    parser.add_argument('id', help='directory id or name')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def unset_directory_variables(id, key):
    headers = {}

    if key is not None:
        key_path = f'?key={key}'
    else:
        key_path = ''

    query = urljoin(Environment().apiSites(), f'{id}/metadata{key_path}')



    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    return []

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