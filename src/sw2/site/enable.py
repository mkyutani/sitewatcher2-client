import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_enable(subparser):
    sp_list = subparser.add_parser('enable', help='enable site')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_enable(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'enabled': True
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