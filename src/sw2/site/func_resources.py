import json
import sys
from sw2.site.list import get_sites
from sw2.site.resource import get_site_resources
from sw2.util import is_uuid

def sw2_parser_site_resources(subparser):
    parser = subparser.add_parser('resources', help='print resources of site')
    parser.add_argument('site', metavar='SITE', help='site id or name')
    parser.add_argument('--json', action='store_true', help='in json format')

def sw2_site_resources(args):
    args_id = args.get('site')
    args_json = args.get('json')

    if is_uuid(args_id):
        ids = [args_id]
    else:
        sites = get_sites(args_id)
        if len(sites) == 0:
            print('Site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in sites]

    result = 0

    for id in ids:
        resources = get_site_resources(id)
        if resources is None:
            result = 1
            continue

        if args_json:
            print(json.dumps(resources))
        else:
            for r in resources:
                print(r['site_name'], r['uri'], r['name'])

    return result