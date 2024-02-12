import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_site_unset(subparser):
    parser = subparser.add_parser('unset', help='unset metadata of site')
    parser.add_argument('id', metavar='ID', help='site id or name')
    parser.add_argument('key', nargs='?', metavar='KEY', default=None, help='metadata key')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_unset(args):
    args_id = args['id']
    args_key = args['key']
    args_strict = args['strict']

    headers = { 'Content-Type': 'application/json' }
    if is_uuid(args_id):
        query = urljoin(Environment().apiSites(), f'{args_id}/metadata/{args_key}')
    else:
        query = urljoin(Environment().apiSites(), f'metadata/{args_key}?name={args_id}')
        if args_strict:
            query = urljoin(query, '&strict=true')

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    return 0