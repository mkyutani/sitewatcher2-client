import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_channel_add(subparser):
    sp_list = subparser.add_parser('add', help='add channel')
    sp_list.add_argument('name', metavar='NAME', help='name')
    sp_list.add_argument('--type', nargs=1, default=['html'], help='type')
    sp_list.add_argument('--disable', action='store_true', help='set disabled')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')

def sw2_channel_add(args, env):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'name': args.name,
        'enabled': 'true' if args.disable else 'false'
    }

    res = None
    try:
        res = requests.post(env.apiChannels(), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    channel = json.loads(res.text)
    print(str(channel["id"]))

    return 0