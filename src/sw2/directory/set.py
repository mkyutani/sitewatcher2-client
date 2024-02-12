import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_directory_set(subparser):
    parser = subparser.add_parser('set', help='set metadata of directory')
    parser.add_argument('id', metavar='ID', help='directory id or name')
    parser.add_argument('key', metavar='KEY', default=None, help='metadata key')
    parser.add_argument('value', nargs='?', metavar='VALUE', default=None, help='metadata value')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='directory name strict mode')

def sw2_directory_set(args):
    args_id = args['id']
    args_key = args['key']
    args_value = args['value'] if args['value'] else ''
    args_json = args['json']
    args_strict = args['strict']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        args_key: args_value
    }
    if is_uuid(args_id):
        query = urljoin(Environment().apiDirectories(), f'{args_id}/metadata')
    else:
        query = urljoin(Environment().apiDirectories(), f'metadata?name={args_id}')
        if args_strict:
            query = urljoin(query, '&strict=true')

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    metadata = json.loads(res.text)
    if args_json:
        print(res.text)
    else:
        for m in metadata:
            message = ' '.join([m['directory'], m['key'], m['value']])
            print(message)

    return 0