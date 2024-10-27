import json
import sys

import yaml
from sw2.site.list import get_sites

def sw2_parser_site_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list sites')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-c', '--command', action='store_true', help='show command template')
    format_group.add_argument('-d', '--detail', action='store_true', help='show detail')
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-r', '--rules-only', action='store_true', help='show rules only')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return aliases

def sw2_site_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_command = args.get('command')
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_rules_only = args.get('rules_only')
    args_yaml = args.get('yaml')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    sites.sort(key=lambda x: x['id'])

    if args_json:
        json.dump(sites, sys.stdout)
    elif args_yaml:
        yaml.dump(sites, sys.stdout)
    else:
        for site in sites:
            if args_rules_only:
                if len(site['rule_category_names']) > 0 or len(site['directory']['rule_category_names']) > 0:
                    print(f'site {site["id"]} {site["name"]}')
                    for site_rule_category_name in site['rule_category_names']:
                        sorted_rules = sorted(site[site_rule_category_name], key=lambda x: x['weight'])
                        for rule in sorted_rules:
                            weight = rule.get('weight')
                            op = rule.get('op')
                            src = rule.get('src')
                            dst = rule.get('dst')
                            value = rule.get('value') if rule.get('value') is not None else ''
                            exp = ':'.join(filter(lambda x: x is not None, [op, dst, src, value]))
                            print(f'- rule {site_rule_category_name} {weight} \'{exp}\'')
                    if len(site['directory']['rule_category_names']) > 0:
                        print(f'- directory {site["directory"]["id"]} {site["directory"]["name"]}')
                        for directory_rule_category_name in site['directory']['rule_category_names']:
                            sorted_rules = sorted(site['directory'][directory_rule_category_name], key=lambda x: x['weight'])
                            for rule in sorted_rules:
                                weight = rule.get('weight')
                                op = rule.get('op')
                                src = rule.get('src')
                                dst = rule.get('dst')
                                value = rule.get('value') if rule.get('value') is not None else ''
                                exp = ':'.join(filter(lambda x: x is not None, [op, dst, src, value]))
                                print(f'  - rule {directory_rule_category_name} {weight} \'{exp}\'')
            elif args_command:
                print(f'# site {site["id"]} {site["name"]}')
                print(f'sw2 site add {site["directory"]["id"]} \'{site["name"]}\' {site["uri"]}')
                for site_rule_category_name in site['rule_category_names']:
                    sorted_rules = sorted(site[site_rule_category_name], key=lambda x: x['weight'])
                    for rule in sorted_rules:
                        weight = rule.get('weight')
                        op = rule.get('op')
                        src = rule.get('src')
                        dst = rule.get('dst')
                        value = rule.get('value') if rule.get('value') is not None else ''
                        exp = ':'.join(filter(lambda x: x is not None, [op, dst, src, value]))
                        print(f'sw2 site set \'{site["directory"]["name"]}:{site["name"]}\' --strict {site_rule_category_name} {weight} \'{exp}\'')
            else:
                print(f'site {site["id"]} {site["name"]}')
                if args_detail:
                    print(f'- uri {site["uri"]}')
                    print(f'- directory {site["directory"]["id"]} {site["directory"]["name"]}')
                    for directory_rule_category_name in site['directory']['rule_category_names']:
                        sorted_rules = sorted(site['directory'][directory_rule_category_name], key=lambda x: x['weight'])
                        for rule in sorted_rules:
                            weight = rule.get('weight')
                            op = rule.get('op')
                            src = rule.get('src')
                            dst = rule.get('dst')
                            value = rule.get('value') if rule.get('value') is not None else ''
                            exp = ':'.join(filter(lambda x: x is not None, [op, dst, src, value]))
                            print(f'  - rule {directory_rule_category_name} {weight} \'{exp}\'')
                    for site_rule_category_name in site['rule_category_names']:
                        sorted_rules = sorted(site[site_rule_category_name], key=lambda x: x['weight'])
                        for rule in sorted_rules:
                            weight = rule.get('weight')
                            op = rule.get('op')
                            src = rule.get('src')
                            dst = rule.get('dst')
                            value = rule.get('value') if rule.get('value') is not None else ''
                            exp = ':'.join(filter(lambda x: x is not None, [op, dst, src, value]))
                            print(f'- rule {site_rule_category_name} {weight} \'{exp}\'')

    return 0