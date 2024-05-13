import sys
from urllib.parse import urljoin
import requests
from sw2.directory.list import get_directories, list_directories
from sw2.env import Environment
from sw2.site.list import get_sites
from sw2.util import is_uuid

def sw2_parser_site_directory(subparser):
    aliases = ['dir']
    parser = subparser.add_parser('directory', aliases=aliases, help='change directory of site')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('directory', metavar='DIR', help='directory id or name')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def sw2_site_directory(args):
    args_name = args.get('name')
    args_directory = args.get('directory')
    args_strict = args.get('strict')
    args_strict_directory = args.get('strict_directory')

    if is_uuid(args_directory):
        directory = args_directory
    else:
        directories = list_directories(args_directory, strict=args_strict_directory)
        if directories is None:
            return 1
        if len(directories) == 0:
            print('Directory not found', file=sys.stderr)
            return 1
        elif len(directories) > 1:
            print('Directory is not unique', file=sys.stderr)
            return 1

        directory = directories[0]['id']

    if is_uuid(args_name):
        ids = [args_name]
    else:
        sites = get_sites(args_name, strict=args_strict)
        if sites is None:
            return 1
        elif len(sites) == 0:
            print('site not found', file=sys.stderr)
            return 1

        ids = [s['id'] for s in sites]

    failures = 0
    for id in ids:
        headers = { 'Content-Type': 'application/json' }
        contents = {
            'directory': directory
        }
        query = urljoin(Environment().apiSites(), id)

        res = None
        try:
            res = requests.put(query, json=contents, headers=headers)
        except Exception as e:
            print(str(e), file=sys.stderr)
            failures = failures + 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            failures = failures + 1

    if failures > 0:
        return 1
    else:
        return 0