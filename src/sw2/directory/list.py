import json
import json
import requests
import sys

from sw2.env import Environment

def sw2_parser_directory_list(subparser):
    parser = subparser.add_parser('list', help='list directories')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory name')
    parser.add_argument('--all', action='store_true', help='include disabled directories')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def get_directories_by_name(name, strict=False, all=False, single=False):
    headers = { 'Cache-Control': 'no-cache' }
    options = []
    if name:
        options.append('='.join(['name', name]))
    if strict:
        options.append('='.join(['strict', 'true']))
    if not all:
        options.append('='.join(['enabled', 'true']))
    query = '?'.join([Environment().apiDirectories(), '&'.join(options)])

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    directories = json.loads(res.text)

    if single:
        if len(directories) == 0:
            print(f'No directory found', file=sys.stderr)
            return None
        elif len(directories) > 1:
            print(f'Multiple directories found', file=sys.stderr)
            return None
        else:
            return directories[0]

    return directories

def sw2_directory_list(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_all = args.get('all')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    directories = get_directories_by_name(args_name, args_strict, args_all)
    if directories is None:
        return 1

    directories.sort(key=lambda x: x['id'])

    if args_json:
        print(json.dumps(directories))
    else:
        for directory in directories:
            print(str(directory['id']), directory['name'], 'enabled' if directory['enabled'] else 'disabled', sep=args_delimiter)

    return 0