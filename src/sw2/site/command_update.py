import json
import sys

from sw2.site.list import get_sites
from sw2.site.update import update_site_resources

def sw2_parser_site_update(subparser):
    parser = subparser.add_parser('update', help='update site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_site_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_push = args.get('push')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    for site in sites:
        resources = update_site_resources(site, push=args_push)
        if resources is None:
            return 1

        if args_json:
            print(json.dumps(resources))
        else:
            if args_push:
                for r in resources:
                    print(r['uri'], ';'.join([f'{x["key"]}={x["value"]}' for x in r['properties']]))
            else:
                for r in resources:
                    print(r['uri'], ';'.join(list(map(lambda x: f'{x}={r["properties"][x]}', r['properties'].keys()))))

    return 0