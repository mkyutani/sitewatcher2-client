import json
import requests
import sys
from urllib.parse import urljoin

from sw2.env import Environment
from sw2.site.list import get_sites

def sw2_parser_site_rules(subparser):
    parser = subparser.add_parser('rules', help='get rules of site')
    parser.add_argument('name', help='site id or name')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')
    return []

def sw2_site_rules(args):
    args_name = args.get('name')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    for site in sites:
        query = urljoin(Environment().apiSites(), '/'.join([site['id'], 'rules']))

        res = None
        try:
            res = requests.get(query)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        if args_json:
            print(res.text)
        else:
            rules = json.loads(res.text)
            for rule in rules:
                print(rule['site'], rule['name'], rule['weight'], rule['value'], sep=args_delimiter)

    return 0