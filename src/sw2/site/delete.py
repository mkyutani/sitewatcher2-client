import sys
from urllib.parse import urljoin
import requests

def sw2_parser_site_delete(subparser):
    sp_list = subparser.add_parser('delete', help='add site')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_site_delete(args, env):
    headers = {}
    query = urljoin(env.apiSites(), args.id)

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