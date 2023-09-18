import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_site_rename(subparser):
    sp_list = subparser.add_parser('rename', help='rename site')
    sp_list.add_argument('id', metavar='ID', help='id')
    sp_list.add_argument('name', metavar='NAME', help='name')

def sw2_site_rename(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args.name
    }
    query = urljoin(env.apiSites(), args.id)

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    return 0