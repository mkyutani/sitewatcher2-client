import json
import sys
from urllib.parse import urljoin
import requests

from sw2.util import isUuid

def sw2_parser_site_unset(subparser):
    parser = subparser.add_parser('unset', help='unset metadata of site')
    parser.add_argument('id', metavar='ID', help='site id or name')
    parser.add_argument('key', nargs='?', metavar='KEY', default=None, help='metadata key')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_unset(args, env):
    id_or_name = args.id
    strict = args.strict
    key = args.key

    headers = { 'Content-Type': 'application/json' }
    if isUuid(id_or_name):
        query = urljoin(env.apiSites(), f'{id_or_name}/metadata/{key}')
    else:
        query = urljoin(env.apiSites(), f'metadata/{key}?name={id_or_name}')
        if strict:
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