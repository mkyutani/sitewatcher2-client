import json
import json
import sys
from sw2.directory.list import get_directories
from sw2.directory.sites import get_sites_by_directory
from sw2.util import is_uuid

def sw2_parser_directory_sites(subparser):
    parser = subparser.add_parser('sites', help='list sites in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_directory_sites(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    if is_uuid(args_name):
        ids = [args_name]
    else:
        directories = get_directories(args_name, strict=args_strict)
        if directories is None:
            return 1
        elif len(directories) == 0:
            print('directory not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in directories]

    sites = []
    for id in ids:
        sites.extend(get_sites_by_directory(id))

    if args_json:
        print(json.dumps(sites))
    else:
        for site in sites:
            print(str(site['directory']), site['directory_name'], str(site['id']), site['name'], site['uri'], sep=args_delimiter)

    return 0