import json
import sys

from sw2.site.list import get_sites
from sw2.site.resources import update_resources

def sw2_parser_site_update(subparser):
    aliases = []
    parser = subparser.add_parser('update', aliases=aliases, help='update site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--test', action='store_true', help='test locally')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]
    args_test = args.get('test')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    for site in sites:
        resources = update_resources(site, test=args_test)
        if resources is None:
            return 1

        if args_json:
            print(json.dumps(resources))
        else:
            if args_test:
                for r in resources:
                    print(r['uri'])
                    properties = r['properties']
                    for key in properties.keys():
                        print('-', key, properties[key], sep=args_delimiter)
            else:
                for r in resources:
                    print(r['uri'])
                    properties = r['properties']
                    for kv in properties:
                        print('-', kv['key'], kv['value'], sep=args_delimiter)

    return 0