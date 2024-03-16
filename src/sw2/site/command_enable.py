import sys

from sw2.util import is_uuid
from sw2.site.list import get_sites
from sw2.site.enable import enable_sites

def sw2_parser_site_enable(subparser):
    parser = subparser.add_parser('enable', help='enable site')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_enable(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    if is_uuid(args_name):
        ids = [args_name]
    else:
        directories = get_sites(args_name, strict=args_strict)
        if directories is None:
            return 1
        elif len(directories) == 0:
            print('site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in directories]

    failures = 0
    for id in ids:
        result = enable_sites(id)
        if result is False:
            print('failed to enable {id}', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0