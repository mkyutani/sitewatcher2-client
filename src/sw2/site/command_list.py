import json
import sys
from sw2.site.list import get_sites

def sw2_parser_site_list(subparser):
    aliases = ['l']
    parser = subparser.add_parser('list', aliases=aliases, help='list sites')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='site id or name')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_site_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_delimiter = args.get('delimiter')[0]
    args_json = args.get('json')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    sites.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(sites))
    else:
        for site in sites:
            print(str(site['id']), site['name'], site['directory_name'], site["uri"], sep=args_delimiter)

    return 0