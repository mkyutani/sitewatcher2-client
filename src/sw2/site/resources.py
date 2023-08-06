import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_resources(subparser):
    sp_list = subparser.add_parser('resources', help='list site resources')
    sp_list.add_argument('id', metavar='ID', help='id')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')

def sw2_resources(args, env):
    headers = {}
    query = urljoin(env.apiSites(), args.id) + '/resources'

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    resources = json.loads(res.text)
    print(resources)
    for resource in resources:
        print(args.delimiter[0].join([str(resource["site"]), resource["name"], resource["uri"]]))

    return 0