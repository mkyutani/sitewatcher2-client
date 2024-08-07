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
    format_group.add_argument('-d', '--detail', action='store_true', help='show detail')
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return aliases

def sw2_site_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_detail = args.get('detail')
    args_json = args.get('json')
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
            print(f'site {site["id"]} {site["name"]}')
            if args_detail:
                print(f'- uri {site["uri"]}')
                print(f'- directory {site["directory"]} {site["directory_name"]}')
                for rule_category_name in site['rule_category_names']:
                    for rule in site[rule_category_name]:
                        print(f'- {rule_category_name} {rule["weight"]} {rule["value"]}')

    return 0