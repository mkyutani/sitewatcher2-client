import requests
import sys
from urllib.parse import urljoin

from sw2.env import Environment
from sw2.site.list import get_sites

def sw2_parser_site_unset(subparser):
    parser = subparser.add_parser('unset', help='unset rule of site')
    parser.add_argument('name', default=None, help='site id or name')
    parser.add_argument('rule', default=None, help='rule name')
    parser.add_argument('weight', default=None, help='rule weight')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

    return []

def sw2_site_unset(args):
    args_name = args.get('name')
    args_rule = args.get('rule').lower()
    args_weight = args.get('weight')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    if args_rule not in ['include', 'exclude', 'start', 'stop', 'property_template']:
        print(f'Invalid rule or expression ({args_rule}, {args_weight})', file=sys.stderr)
        return 1

    for site in sites:
        query = urljoin(Environment().apiSites(), '/'.join([site['id'], 'rules', args_rule, args_weight]))

        res = None
        try:
            res = requests.delete(query)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        print(site['id'], site['name'], args_rule, args_weight)

    return 0