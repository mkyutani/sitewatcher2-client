import json
import sys
from urllib.parse import urljoin
import requests

from sw2.util import isUuid

def sw2_parser_site_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of site')
    parser.add_argument('id', metavar='ID', help='site id or name')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_variables(args, env):
    id_or_name = args.id
    strict = args.strict

    if isUuid(id_or_name):
        query = urljoin(env.apiSites(), f'{id_or_name}/metadata')
    else:
        query = urljoin(env.apiSites(), f'metadata?name={id_or_name}')
        if strict:
            query = urljoin(query, '&strict=true')

    res = None
    try:
        res = requests.get(query)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    metadata = json.loads(res.text)
    if args.json:
        print(res.text)
    else:
        for m in metadata:
            message = ' '.join([m['site'], m['key'], m['value']])
            print(message)

    return 0