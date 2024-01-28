import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_directory_metadata(subparser):
    parser = subparser.add_parser('metadata', help='update metadata of directory')
    parser.add_argument('id', metavar='ID', help='id')
    parser.add_argument('key', nargs='?', metavar='KEY', default=None, help='metadata key')
    parser.add_argument('value', nargs='?', metavar='VALUE', default=None, help='metadata value')

def sw2_directory_metadata_set(id, key, value, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        key: value
    }
    query = urljoin(urljoin(env.apiDirectories(), f'{id}/'), 'metadata')

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    metadata = json.loads(res.text)[0]
    message = ' '.join([metadata['directory'], metadata['key'], metadata['value']])
    print(message)

    return 0

def sw2_directory_metadata_unset(id, key, env):
    headers = { 'Content-Type': 'application/json' }
    query = urljoin(urljoin(urljoin(env.apiDirectories(), f'{id}/'), 'metadata/'), f'{key}')

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    return 0

def sw2_directory_metadata_list(id, env):
    query = urljoin(urljoin(env.apiDirectories(), f'{id}/'), 'metadata')

    res = None
    try:
        res = requests.get(query)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    metadata = json.loads(res.text)
    for m in metadata:
        message = ' '.join([m['directory'], m['key'], m['value']])
        print(message)

    return 0

def sw2_directory_metadata(args, env):
    if args.key is None:
        return sw2_directory_metadata_list(args.id, env)
    elif args.value is None:
        return sw2_directory_metadata_unset(args.id, args.key, env)
    else:
        return sw2_directory_metadata_set(args.id, args.key, args.value, env)