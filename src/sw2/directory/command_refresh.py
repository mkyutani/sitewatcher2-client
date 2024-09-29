import json
import sys

import yaml

from sw2.directory.list import get_directories
from sw2.site.list import get_site
from sw2.site.resources import refresh_resources

def sw2_parser_directory_refresh(subparser):
    parser = subparser.add_parser('refresh', help='refresh site resource properties')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def sw2_directory_refresh(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    directories.sort(key=lambda x: x['id'])

    for directory in directories:
        print(f'directory {directory["id"]} {directory["name"]}')

        for site in directory['sites']:
            print(f'site {site["id"]} {site["name"]}')

            site = get_site(site['id'])
            if site is None:
                return 1

            resources = refresh_resources(site)
            if resources is None:
                return 1

            for resource in resources:
                name = 'None'
                for kv in resource['properties']:
                    if kv['key'] == '_name':
                        name = kv['value']
                        break
                print(f'resource {resource["id"]} {name}')
                print(f'- uri {resource["uri"]}')
                print(f'- site {resource["site"]} {resource["site_name"]}')
                print(f'- timestamp {resource["timestamp"]}')
                for kv in resource['properties']:
                    print(f'- property {kv["key"]} {kv["value"]}')

    return 0