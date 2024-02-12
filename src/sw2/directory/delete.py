import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def sw2_parser_directory_delete(subparser):
    sp_list = subparser.add_parser('delete', help='add directory')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_directory_delete(args):
    args_id = args['id']

    headers = {}
    query = urljoin(Environment().apiDirectories(), args_id)

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    return 0