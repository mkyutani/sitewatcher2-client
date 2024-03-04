import json
import json
from sw2.directory.list import get_directories
from sw2.directory.sites import get_sites_by_directory

def sw2_parser_directory_sites(subparser):
    parser = subparser.add_parser('sites', help='list sites in directory')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory name')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    parser.add_argument('--all', action='store_true', help='include disabled directories')
    parser.add_argument('--sort', action='store_true', help='sort by name')

def sw2_directory_sites(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_all = args.get('all')
    args_sort = args.get('sort')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    directories = get_directories(args_name, args_strict, args_all)

    sites = []
    for directory in directories:
        sites.extend(get_sites_by_directory(directory['id']))

    if args_sort:
        sites.sort(key=lambda x: x['name'])

    if args_json:
        print(json.dumps(sites))
    else:
        for site in sites:
            print(str(site['id']), site['name'], site['uri'], sep=args_delimiter)

    return 0