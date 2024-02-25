import json
import sys
from sw2.site.list import get_sites
from sw2.site.set import set_site_variables
from sw2.util import is_uuid

def sw2_parser_site_set(subparser):
    parser = subparser.add_parser('set', help='set metadata of site')
    parser.add_argument('id', help='site id or name')
    parser.add_argument('key', default=None, help='metadata key')
    parser.add_argument('value', default=None, help='metadata value')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_set(args):
    args_id = args.get('id')
    args_key = args.get('key')
    args_value = args.get('value') if args.get('value') else ''
    args_json = args.get('json')
    args_strict = args.get('strict')

    if is_uuid(args_id):
        ids = [args_id]
    else:
        sites = get_sites(args_id, strict=args_strict)
        if len(sites) == 0:
            print('Site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in sites]

    ids.sort()

    for id in ids:
        metadata = set_site_variables(id, args_key, args_value)
        if metadata is not None:
            metadata.sort(key=lambda x: x['key'])
            if args_json:
                print(json.dumps(metadata))
            else:
                for m in metadata:
                    message = ' '.join([m['site'], m['key'], m['value']])
                    print(message)

    return 0