import sys

from sw2.util import is_uuid
from sw2.site.list import get_sites
from sw2.site.delete import delete_site

def sw2_parser_site_delete(subparser):
    parser = subparser.add_parser('delete', help='add site')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')
    return []

def sw2_site_delete(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        ids = [args_name]
    else:
        sites = get_sites(args_name, strict=args_strict)
        if sites is None:
            return 1
        elif len(sites) == 0:
            print('site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in sites]

    failures = 0
    for id in ids:
        result = delete_site(id)
        if result is False:
            print('failed to delete {id}', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0