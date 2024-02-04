import json
import sys
from urllib.parse import urljoin
import requests

from sw2.util import isUuid

def sw2_parser_site_set(subparser):
    parser = subparser.add_parser('set', help='set metadata of site')
    parser.add_argument('id', metavar='ID', help='site id or name')
    parser.add_argument('key', metavar='KEY', default=None, help='metadata key')
    parser.add_argument('value', nargs='?', metavar='VALUE', default=None, help='metadata value')
    parser.add_argument('--strict', action='store_true', help='site name strict mode')

def sw2_site_set(args, env):
    id_or_name = args.id
    strict = args.strict
    key = args.key
    if args.value is not None:
        value = args.value
    else:
        value = ''

    headers = { 'Content-Type': 'application/json' }
    contents = {
        key: value
    }
    if isUuid(id_or_name):
        query = urljoin(env.apiSites(), f'{id_or_name}/metadata')
    else:
        query = urljoin(env.apiSites(), f'metadata?name={id_or_name}')
        if strict:
            query = urljoin(query, '&strict=true')

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

    metadata = json.loads(res.text)[0]
    message = ' '.join([metadata['site'], metadata['key'], metadata['value']])
    print(message)

    return 0