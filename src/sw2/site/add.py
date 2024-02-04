import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_site_add(subparser):
    sp_list = subparser.add_parser('add', help='add site')
    sp_list.add_argument('directory', metavar='DIR', help='directory id')
    sp_list.add_argument('name', metavar='NAME', help='name')
    sp_list.add_argument('uri', metavar='URI', help='source uri')
    sp_list.add_argument('--disable', action='store_true', help='set disabled')

def sw2_site_add(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args.name,
        'uri': args.uri,
        'directory': args.directory,
        'enabled': 'true' if not args.disable else 'false'
    }

    res = None
    try:
        res = requests.post(env.apiSites(), json=contents, headers=headers)
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