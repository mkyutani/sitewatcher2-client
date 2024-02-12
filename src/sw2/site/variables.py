import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment
from sw2.util import is_uuid

def sw2_parser_site_variables(subparser):
    parser = subparser.add_parser('variables', help='update metadata of site')
    parser.add_argument('id', metavar='ID', help='site id or name')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_variables(args):
    args_id = args.get('id')
    args_json = args.get('json')
    args_strict = args.get('strict')

    if is_uuid(args_id):
        query = urljoin(Environment().apiSites(), f'{args_id}/metadata')
    else:
        query = urljoin(Environment().apiSites(), f'metadata?name={args_id}')
        if args_strict:
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
    if args_json:
        print(res.text)
    else:
        for m in metadata:
            message = ' '.join([m['site'], m['key'], m['value']])
            print(message)

    return 0