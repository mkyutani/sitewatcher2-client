import json
import json
import sys

import yaml

from sw2.directory.list import get_directories
from sw2.site.list import get_site
from sw2.site.resources import update_resources

def sw2_parser_directory_update(subparser):
    aliases = []
    parser = subparser.add_parser('update', aliases=aliases, help='update site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_directory_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    for directory in directories:
        print(f'directory {directory["id"]} {directory["name"]}')

        for site in directory['sites']:
            print(f'site {site["id"]} {site["name"]}')

            site = get_site(site['id'])
            if site is None:
                return 1

            resources = update_resources(site)
            if resources is None:
                return 1

            for resource in resources:
                name = 'None'
                for kv in resource['properties']:
                    if kv['key'] == 'name':
                        name = kv['value']
                        break
                print(f'resource {resource["id"]} {name}')
                print(f'- uri {resource["uri"]}')
                print(f'- site {resource["site"]} {resource["site_name"]}')
                print(f'- timestamp {resource["timestamp"]}')
                for kv in resource['properties']:
                    print(f'- property {kv["key"]} {kv["value"]}')

    return 0