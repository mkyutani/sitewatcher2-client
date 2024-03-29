import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_site_rename(subparser):
    parser = subparser.add_parser('rename', help='rename site')
    parser.add_argument('id', metavar='ID', help='id')
    parser.add_argument('name', metavar='NAME', help='name')

def sw2_site_rename(args):
    args_id = args.get('id')
    args_name = args.get('name')

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name
    }
    query = urljoin(Environment().apiSites(), args_id)

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