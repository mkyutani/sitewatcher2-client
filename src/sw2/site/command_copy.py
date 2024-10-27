import json
import sys
from urllib.parse import urljoin

import requests
import yaml
from sw2.env import Environment
from sw2.site.list import get_sites

def sw2_parser_site_copy(subparser):
    aliases = []
    parser = subparser.add_parser('copy', aliases=aliases, help='copy site rules')
    parser.add_argument('name', nargs=1, metavar='NAME', default=None, help='destination site id, name or "all"')
    parser.add_argument('source', nargs=1, metavar='SOURCE', default=None, help='source site id or name')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_copy(args):
    args_name = args.get('name')[0]
    args_source = args.get('source')[0]
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    sites.sort(key=lambda x: x['id'])

    sources = get_sites(args_source, strict=args_strict)
    if sources is None:
        return 1
    elif len(sources) == 0:
        print('site not found', file=sys.stderr)
        return 1
    elif len(sources) > 1:
        print('multiple sites found', file=sys.stderr)
        return 1

    source = sources[0]
    site_rule_category_names = source['rule_category_names']
    rules = []
    for site_rule_category_name in site_rule_category_names:
        sorted_source_rules = sorted(source[site_rule_category_name], key=lambda x: x['weight'])
        for source_rule in sorted_source_rules:
            rule = {}
            rule['category_name'] = site_rule_category_name
            rule['weight'] = source_rule.get('weight')
            rule['op'] = source_rule.get('op')
            rule['src'] = source_rule.get('src')
            rule['dst'] = source_rule.get('dst')
            rule['value'] = source_rule.get('value') if source_rule.get('value') is not None else ''
            rules.append(rule)

    headers = { 'Content-Type': 'application/json' }

    print(rules)

    for site in sites:
        for rule in rules:
            query = urljoin(Environment().apiSites(), '/'.join([site['id'], 'rules', rule['category_name'], str(rule['weight'])]))
            contents = {}
            if rule.get('op'):
                contents['op'] = rule.get('op')
            if rule.get('src'):
                contents['src'] = rule.get('src')
            if rule.get('dst'):
                contents['dst'] = rule.get('dst')
            if rule.get('value'):
                contents['value'] = rule.get('value')
            else:
                contents['value'] = ''

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

            destination_rules = res.json()
            print(site['id'], site['name'], destination_rules['category_name'], destination_rules['weight'])

    return 0