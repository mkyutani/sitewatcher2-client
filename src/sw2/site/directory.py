import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment
from sw2.func import get_directories
from sw2.util import is_uuid

def sw2_parser_site_directory(subparser):
    parser = subparser.add_parser('directory', help='change directory of site')
    parser.add_argument('id', metavar='ID', help='id')
    parser.add_argument('directory', metavar='DIR', help='directory id or name')

def sw2_site_directory(args):
    args_id = args['id']
    args_directory = args['directory']

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
        'directory': directory
    }
    query = urljoin(Environment().apiSites(), args_id)

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    return 0