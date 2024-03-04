import json

from sw2.directory.list import get_directories

def sw2_parser_directory_list(subparser):
    parser = subparser.add_parser('list', help='list directories')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory name')
    parser.add_argument('--all', action='store_true', help='include disabled directories')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--metadata', action='store_true', help='include metadata')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_directory_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_all = args.get('all')
    args_json = args.get('json')
    args_metadata = args.get('metadata')
    args_delimiter = args.get('delimiter')[0]

    directories = get_directories(args_name, args_strict, args_all, args_metadata)
    if directories is None:
        return 1

    directories.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(directories))
    else:
        for directory in directories:
            print(str(directory['id']), directory['name'], 'enabled' if directory['enabled'] else 'disabled', sep=args_delimiter)

    return 0