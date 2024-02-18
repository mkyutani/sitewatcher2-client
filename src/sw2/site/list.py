import json
import json
from urllib.parse import urljoin
import requests
import sys

from sw2.env import Environment

def sw2_parser_site_list(subparser):
    sp_list = subparser.add_parser('list', help='list sites')
    sp_list.add_argument('name', nargs='?', metavar='NAME', default=None, help='site name')
    sp_list.add_argument('--all', action='store_true', help='include disabled sites')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    sp_list.add_argument('--json', action='store_true', help='in json format')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')

def get_site(id):
    headers = { 'Cache-Control': 'no-cache' }

    query = urljoin(Environment().apiSites(), id)

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    site = json.loads(res.text)

    return site

def get_sites_by_name(name, strict=False, all=False, single=False):
    headers = { 'Cache-Control': 'no-cache' }
    options = []
    if name:
        options.append('='.join(['name', name]))
    if strict:
        options.append('='.join(['strict', 'true']))
    if not all:
        options.append('='.join(['enabled', 'true']))
    query = '?'.join([Environment().apiSites(), '&'.join(options)])

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    sites = json.loads(res.text)

    if single:
        if len(sites) == 0:
            print(f'No directory found', file=sys.stderr)
            return None
        elif len(sites) > 1:
            print(f'Multiple directories found', file=sys.stderr)
            return None
        else:
            return sites[0]

    return sites

def sw2_site_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_delimiter = args.get('delimiter')[0]
    args_json = args.get('json')
    args_all = args.get('all')

    sites = get_sites_by_name(args_name, args_strict, args_all)
    if sites is None:
        return 1

    sites.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(sites))
    else:
        for site in sites:
            print(str(site['id']), site['name'], site['directory_name'], site["uri"], 'enabled' if site['enabled'] else 'disabled', sep=args_delimiter)

    return 0