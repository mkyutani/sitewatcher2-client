import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_delete(subparser):
    sp_list = subparser.add_parser('delete', help='add site')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_delete(args, env):

    headers = {}
    query = urljoin(env.apiSites(), args.id)
    print(query)

    try:
        requests.delete(query, headers=headers)
    except Exception as e:
        print(f'Failed to fetch: {str(e)}', file=sys.stderr)
        return 1

    return 0