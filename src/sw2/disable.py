import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_disable(subparser):
    sp_list = subparser.add_parser('disable', help='disable site')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_disable(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'enabled': False
    }
    query = urljoin(env.apiSites(), args.id)

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
    except Exception as e:
        print(f'Failed to fetch: {str(e)}', file=sys.stderr)
        return 1

    if res.status_code >= 400:
        print(f'Failed to disable: {res.status_code} {res.text}', file=sys.stderr)
        return 1

    return 0