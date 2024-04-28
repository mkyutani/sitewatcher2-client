import json
import sys
from sw2.site.list import get_sites
from sw2.site.variables import get_site_variables
from sw2.util import is_uuid

def sw2_parser_site_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of site')
    parser.add_argument('id', help='site id or name')
    parser.add_argument('key', nargs='?', default=None, help='metadata key')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_variables(args):
    args_id = args.get('id')
    args_key = args.get('key')
    args_json = args.get('json')
    args_strict = args.get('strict')

    if is_uuid(args_id):
        ids = [args_id]
    else:
        sites = get_sites(args_id, strict=args_strict)
        if sites is None:
            return 1
        elif len(sites) == 0:
            print('Site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in sites]

    ids.sort()

    all_metadata = []
    for id in ids:
        metadata = get_site_variables(id, args_key)
        if metadata is None:
            return 1

        all_metadata.extend(metadata)

    if args_json:
        print(json.dumps(all_metadata))
    else:
        for m in all_metadata:
            message = ' '.join([m['site'], m['site_name'], m['key'], m['value']])
            print(message)
    return 0