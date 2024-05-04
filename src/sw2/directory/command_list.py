import json
import sys

from sw2.directory.list import get_directories

def sw2_parser_directory_list(subparser):
    parser = subparser.add_parser('list', help='list directories')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--sites', action='store_true', help='list sites')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_directory_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_sites = args.get('sites')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    directories.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(directories))
    else:
        for directory in directories:
            print(str(directory['id']), directory['name'], sep=args_delimiter)
            if args_sites:
                for site in directory['sites']:
                    print(' ', str(site['id']), site['name'], sep=args_delimiter)

    return 0