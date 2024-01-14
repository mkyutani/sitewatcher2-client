import sys
from urllib.parse import urljoin
import requests

def sw2_parser_directory_metadata(subparser):
    parser = subparser.add_parser('metadata', help='update metadata of directory')
    parser.add_argument('id', metavar='ID', help='id')
    parser.add_argument('metadata', metavar='METADATA', help='metadata')

def sw2_directory_metadata(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'metadata': args.metadata
    }
    query = urljoin(env.apiDirectories(), args.id)

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

    return 0