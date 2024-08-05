import json
import sys
import yaml

from sw2.site.list import get_sites
from sw2.site.resources import test_resources

def sw2_parser_site_test(subparser):
    aliases = []
    parser = subparser.add_parser('test', aliases=aliases, help='test site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_test(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    for site in sites:
        print(f'site {site["id"]} {site["name"]}')

        resources = test_resources(site)
        if resources is None:
            return 1

        for resource in resources:
            print(f'resource test {resource["name"]}')
            print(f'- uri {resource["uri"]}')
            properties = resource['properties']
            for key in properties.keys():
                print(f'- property {key} {properties[key]}')

    return 0