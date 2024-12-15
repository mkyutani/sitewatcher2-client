import json
import sys

import yaml

from sw2.site.list import get_sites
from sw2.site.resources import update_resources

def sw2_parser_site_update(subparser):
    aliases = []
    parser = subparser.add_parser('update', aliases=aliases, help='update site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    sites.sort(key=lambda x: x['id'])

    for site in sites:
        print(f'site {site["id"]} {site["name"]}')

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