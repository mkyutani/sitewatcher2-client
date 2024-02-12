import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_directory_add(subparser):
    sp_list = subparser.add_parser('add', help='add directory')
    sp_list.add_argument('name', metavar='NAME', help='name')
    sp_list.add_argument('--disable', action='store_true', help='set disabled')

def sw2_directory_add(args):
    args_name = args['name']
    args_disable = args['disable']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
        'enabled': 'true' if not args_disable else 'false'
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