import requests
import sys
from urllib.parse import urljoin

from sw2.env import Environment
from sw2.site.list import get_sites

def sw2_parser_site_set(subparser):
    parser = subparser.add_parser('set', help='set rule of site')
    parser.add_argument('name', help='site id or name')
    parser.add_argument('rule', help='rule name (include, exclude, or property_template)')
    parser.add_argument('weight', help='rule weight')
    parser.add_argument('expression', help='rule expression (src:value for include and exclude; "set":dst:value, "match":dst:src:value, or "none" for property_template)')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')
    return []

def sw2_site_set(args):
    args_name = args.get('name')
    args_rule = args.get('rule').lower()
    args_weight = str(int(args.get('weight')))
    args_expression = args.get('expression')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    headers = { 'Content-Type': 'application/json' }
    contents = {}

    try:
        if args_rule in ['include', 'exclude', 'start', 'stop']:
            src, value = args_expression.split(':', 1)
            contents['op'] = None
            contents['src'] = src
            contents['dst'] = None
            contents['value'] = value
        elif args_rule == 'walk':
            dst, value = args_expression.split(':', 1)
            contents['op'] = None
            contents['src'] = None
            contents['dst'] = dst.strip()
            contents['value'] = value
        elif args_rule == 'property_template':
            op, expr = args_expression.split(':', 1)
            op = op.strip().lower()
            if op not in ['set', 'match', 'none']:
                raise ValueError()
            contents['op'] = op
            if op == 'set':
                dst, value = expr.split(':', 1)
                contents['src'] = None
                contents['dst'] = dst.strip()
                contents['value'] = value
            elif op == 'match':
                dst, src, value = expr.split(':', 2)
                contents['src'] = src.strip()
                contents['dst'] = dst.strip()
                contents['value'] = value
            else:
                raise ValueError()
        else:
            raise ValueError()
    except ValueError:
        if args_expression.lower() == 'none':
            contents['op'] = 'none'
            contents['src'] = None
            contents['dst'] = None
            contents['value'] = None
        else:
            print(f'Invalid rule or expression ({args_rule}, {args_weight})', file=sys.stderr)
            return 1

    for site in sites:
        query = urljoin(Environment().apiSites(), '/'.join([site['id'], 'rules', args_rule, args_weight]))

        res = None
        try:
            res = requests.post(query, json=contents, headers=headers)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        rule = res.json()
        print(site['id'], site['name'], rule['category_name'], rule['weight'])

    return 0