import json
import json
import sys

import yaml

from sw2.directory.list import get_directories
from sw2.site.list import get_site
from sw2.site.resources import test_resources

def sw2_parser_directory_test(subparser):
    aliases = []
    parser = subparser.add_parser('test', aliases=aliases, help='test site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--all', action='store_true', help='include known resources')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_directory_test(args):
    args_name = args.get('name')
    args_all = args.get('all')
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

            resources = test_resources(site, all=args_all)
            if resources is None:
                return 1

            for resource in resources:
                print(f'resource test {resource["name"]}')
                print(f'- uri {resource["uri"]}')
                properties = resource['properties']
                for key in properties.keys():
                    print(f'- property {key} {properties[key]}')

    return 0