import json
import sys
import requests
from sw2.directory.list import get_directories
from sw2.env import Environment
from sw2.site.update import update_site_resources
from sw2.site.list import get_sites

def sw2_parser_site_add(subparser):
    parser = subparser.add_parser('add', help='add site')
    parser.add_argument('directory', metavar='DIR', help='directory id or name')
    parser.add_argument('name', metavar='NAME', help='name')
    parser.add_argument('uri', metavar='URI', help='source uri')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')

def sw2_site_add(args):
    args_directory = args.get('directory')
    args_name = args.get('name')
    args_uri = args.get('uri')
    args_delimiter = args.get('delimiter')[0]
    args_json = args.get('json')

    directories = get_directories(args_directory, single=True)
    if directories is None:
        return 1

    directory = directories['id']
    directory_name = directories['name']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args_name,
        'uri': args_uri,
        'directory': directory
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

    messages_diff = []
    messages = update_site_resources(site['id'], push=True, initial=True)
    for message in messages:
        if message['op'] in '+-':
            messages_diff.append(message)

    site_info = get_sites(site['id'], single=True)
    if site_info:
        site = site_info
    else:
        site['name'] = args_name
        site['uri'] = args_uri
        site['directory_name'] = directory_name

    if args_json: 
        print(json.dumps({
            'site': site,
            'resources': messages_diff
        }))
    else:
        print(str(site['id']), site['name'], site['directory_name'], site["uri"], sep=args_delimiter)
        for message in messages:
            if message['op'] in '+-':
                print(message['op'], message['message'])

    return 0