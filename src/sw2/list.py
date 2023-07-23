import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_list(subparser):
    sp_list = subparser.add_parser('list', help='list sites')
    sp_list.add_argument('name', nargs='?', metavar='NAME', default=None, help='site name')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    sp_list.add_argument('--long', action='store_true', help='in long format')

def sw2_list(args, env):

    headers = { 'Cache-Control': 'no-cache' }
    options = []
    if args.name:
        options.append('='.join(['name', args.name]))
    if args.strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([env.apiSites(), '&'.join(options)])

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(f'Failed to fetch: {str(e)}', file=sys.stderr)
        return 1

    if res.status_code >= 400:
        print('Failed to fetch ({})'.format(res.status_code), file=sys.stderr)
        return 1

    sites = json.loads(res.text)
    for site in sites:
        if args.long:
            print(args.delimiter[0].join([str(site["id"]), site["name"], site["uri"], site["type"], str(site["enabled"]), site["created"], site["updated"]]))
        else:
            print(args.delimiter[0].join([str(site["id"]), site["name"], site["uri"]]))

    return 0