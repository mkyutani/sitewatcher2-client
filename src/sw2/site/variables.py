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

def get_site_variables(id, key=None, strict=False):
    if key is not None:
        key_path = f'/{key}'
    else:
        key_path = ''

    if is_uuid(id):
        query = urljoin(Environment().apiSites(), f'{id}/metadata{key_path}')
    else:
        query = urljoin(Environment().apiSites(), f'metadata{key_path}?name={id}')
        if strict:
            query = urljoin(query, '&strict=true')

    res = None
    try:
        res = requests.get(query)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    metadata = json.loads(res.text)

    return metadata

def sw2_site_variables(args):
    args_id = args.get('id')
    args_json = args.get('json')
    args_strict = args.get('strict')

    metadata = get_site_variables(args_id, strict=args_strict)
    if metadata is None:
        return 1

    if args_json:
        print(json.dumps(metadata))
    else:
        for m in metadata:
            message = ' '.join([m['site'], m['key'], m['value']])
            print(message)

    return 0