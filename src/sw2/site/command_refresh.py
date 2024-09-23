import sys

from sw2.site.list import get_sites
from sw2.site.resources import refresh_resources

def sw2_parser_site_refresh(subparser):
    aliases = []
    parser = subparser.add_parser('refresh', aliases=aliases, help='refresh site resource properties')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_refresh(args):
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