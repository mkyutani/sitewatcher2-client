import json
import sys
from urllib.parse import urljoin
import requests
from sw2.directory.list import get_directories
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_site_add(subparser):
    parser = subparser.add_parser('add', help='add site')
    parser.add_argument('directory', metavar='DIR', help='directory id or name')
    parser.add_argument('name', metavar='NAME', help='name')
    parser.add_argument('uri', metavar='URI', help='source uri')
    parser.add_argument('--disable', action='store_true', help='set disabled')

def sw2_site_add(args):
    args_directory = args.get('directory')
    args_name = args.get('name')
    args_uri = args.get('uri')
    args_disable = args.get('disable')

    if is_uuid(args_directory):
        directory = args_directory
    else:
        directories = get_directories(args_directory)
        if len(directories) == 0:
            print('Directory not found', file=sys.stderr)
            return 1
        elif len(directories) > 1:
            print('Directory is not unique', file=sys.stderr)
            return 1

        directory = directories[0]['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
        'uri': args_uri,
        'directory': directory,
        'enabled': 'true' if not args_disable else 'false'
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
    print(str(site["id"]))

    return 0