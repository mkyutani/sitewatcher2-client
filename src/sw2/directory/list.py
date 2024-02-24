import json
import json
import requests
import sys

from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_directory_list(subparser):
    parser = subparser.add_parser('list', help='list directories')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='directory name')
    parser.add_argument('--all', action='store_true', help='include disabled directories')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--metadata', action='store_true', help='include metadata')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def get_directories(name, strict=False, all=False, metadata=False, single=False):
    if name and name.lower() == 'all':
        name = None

    headers = { 'Cache-Control': 'no-cache' }
    id = ''
    options = []
    if name:
        if is_uuid(name):
            id = name
        else:
            options.append('='.join(['name', name]))
    if strict:
        options.append('='.join(['strict', 'true']))
    if all:
        options.append('='.join(['all', 'true']))
    if metadata:
        options.append('='.join(['metadata', 'true']))
    query = '?'.join([Environment().apiDirectories() + id, '&'.join(options)])

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
    else:
        if type(directories) is dict:
            directories = [directories]
        return directories

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