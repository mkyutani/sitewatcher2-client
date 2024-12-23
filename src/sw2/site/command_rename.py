import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.site.list import get_sites

def sw2_parser_site_rename(subparser):
    parser = subparser.add_parser('rename', help='rename site')
    parser.add_argument('name', metavar='NAME', help='old name')
    parser.add_argument('new', metavar='NEW', help='new name')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def sw2_site_rename(args):
    args_name = args.get('name')
    args_new = args.get('new')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1
    elif len(sites) > 1:
        print('ambiguous site name', file=sys.stderr)
        return 1

    id = sites[0]['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_new
    }
    query = urljoin(Environment().apiSites(), id)

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

    site = json.loads(res.text)
    print(f'{site["id"]} {site["name"]}')

    return 0