import json
import json
import sys

import yaml

from sw2.directory.list import get_directories
from sw2.site.resources import get_resources

def sw2_parser_directory_resources(subparser):
    aliases = []
    parser = subparser.add_parser('resources', aliases=aliases, help='get site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-d', '--detail', action='store_true', help='show detail')
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return aliases

def sw2_directory_resources(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_yaml = args.get('yaml')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    all_site_resources = []
    result = 0

    for directory in directories:
        print(f'directory {directory["id"]} {directory["name"]}', file=sys.stderr)

        for site in directory['sites']:
            print(f'site {site["id"]} {site["name"]}', file=sys.stderr)
        
            resources = get_resources(site['id'])
            if resources is None:
                result = 1
                continue

            for resource in resources:
                all_site_resources.append(resource)

    if args_json:
        json.dump(all_site_resources, sys.stdout)
    elif args_yaml:
        yaml.dump(all_site_resources, sys.stdout)
    else:
        for resource in all_site_resources:
            name = 'None'
            for kv in resource['properties']:
                if kv['key'] == 'name':
                    name = kv['value']
                    break
            print(f'resource {resource["id"]} {name}')
            if args_detail:
                print(f'- uri {resource["uri"]}')
                print(f'- site {resource["site"]} {resource["site_name"]}')
                print(f'- timestamp {resource["timestamp"]}')
                for kv in resource['properties']:
                    print(f'- property {kv["key"]} {kv["value"]}')

    return result