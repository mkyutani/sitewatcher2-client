import sys
from urllib.parse import urljoin
import requests

def sw2_parser_channel_delete(subparser):
    sp_list = subparser.add_parser('delete', help='delete channel')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_channel_delete(args, env):
    headers = {}
    query = urljoin(env.apiChannels(), args.id)

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