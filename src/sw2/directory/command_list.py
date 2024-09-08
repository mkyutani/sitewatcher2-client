import json
import sys

import yaml

from sw2.directory.list import get_directories

def sw2_parser_directory_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list directories')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-d', '--detail', action='store_true', help='show detail')
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-s', '--sites', action='store_true', help='show sites')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return aliases

def sw2_directory_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_sites = args.get('sites')
    args_yaml = args.get('yaml')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    directories.sort(key=lambda x: x['id'])

    if args_json:
        json.dump(directories, sys.stdout)
    elif args_yaml:
        yaml.dump(directories, sys.stdout)
    else:
        for directory in directories:
            print(f'directory {directory["id"]} {directory["name"]}')
            if args_detail:
                for rule_category_name in directory['rule_category_names']:
                    sorted_rules = sorted(directory[rule_category_name], key=lambda x: x['weight'])
                    for rule in sorted_rules:
                        exp = ' '.join(filter(lambda x: x is not None, [rule['op'], rule['dst'], rule['src'], rule['value']]))
                        print(f'- rule {rule_category_name} {rule["weight"]} {exp}')
            if args_sites:
                for site in directory['sites']:
                    print(f'- site {site["id"]} {site["name"]}')
    return 0