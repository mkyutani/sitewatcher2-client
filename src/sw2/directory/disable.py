import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_directory_disable(subparser):
    parser = subparser.add_parser('disable', help='disable directory')
    parser.add_argument('id', metavar='ID', help='id')

def sw2_directory_disable(args):
    args_id = args.get('id')

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'enabled': False
    }
    query = urljoin(Environment().apiDirectories(), args_id)

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

    return 0