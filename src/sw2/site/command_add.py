import json
import sys
import requests
from sw2.directory.list import list_directories
from sw2.env import Environment

def sw2_parser_site_add(subparser):
    parser = subparser.add_parser('add', help='add site')
    parser.add_argument('directory', metavar='DIR', help='directory id or name')
    parser.add_argument('name', metavar='NAME', help='name')
    parser.add_argument('uri', metavar='URI', help='source uri')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    return []

def sw2_site_add(args):
    args_directory = args.get('directory')
    args_name = args.get('name')
    args_uri = args.get('uri')
    args_delimiter = args.get('delimiter')[0]
    args_json = args.get('json')

    directories = list_directories(args_directory)
    if directories is None:
        return 1
    if len(directories) == 0:
        print(f'no such directory: {args_directory}', file=sys.stderr)
        return 1

    directory = directories[0]
    directory_id = directory['id']
    directory_name = directory['name']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
        'uri': args_uri,
        'directory': directory_id
    }

    res = None
    try:
        res = requests.post(Environment().apiSites(), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    site = json.loads(res.text)
    print(str(site['id']))

    return 0