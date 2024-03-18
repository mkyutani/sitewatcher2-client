import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_directory_add(subparser):
    parser = subparser.add_parser('add', help='add directory')
    parser.add_argument('name', metavar='NAME', help='name')

def sw2_directory_add(args):
    args_name = args.get('name')

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
    }

    res = None
    try:
        res = requests.post(Environment().apiDirectories(), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    directory = json.loads(res.text)
    print(str(directory['id']))

    return 0