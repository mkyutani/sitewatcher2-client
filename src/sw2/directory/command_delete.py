import json
import sys
from urllib.parse import urljoin
import requests

from sw2.directory.list import get_directories
from sw2.env import Environment

def sw2_parser_directory_delete(subparser):
    parser = subparser.add_parser('delete', help='add directory')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def sw2_directory_delete(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    for directory in directories:
        headers = {}
        query = urljoin(Environment().apiDirectories(), directory['id'])

        res = None
        try:
            res = requests.delete(query, headers=headers)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(message, file=sys.stderr)
            return 1

        deleted = json.loads(res.text)
        print(deleted["id"])

    return 0