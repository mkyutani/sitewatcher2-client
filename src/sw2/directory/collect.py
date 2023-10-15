import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_directory_collect(subparser):
    sp_list = subparser.add_parser('collect', help='create a collector')
    sp_list.add_argument('target', metavar='TARGET', help='target directory id')

def sw2_directory_collect(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'target': args.target
    }
    print(env.apiDirectoryCollectors(), file=sys.stderr)

    res = None
    try:
        res = requests.post(env.apiDirectoryCollectors(), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    directory = json.loads(res.text)
    print(str(directory["id"]))

    return 0