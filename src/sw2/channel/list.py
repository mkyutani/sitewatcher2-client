import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_channel_list(subparser):
    sp_list = subparser.add_parser('list', help='list channels')
    sp_list.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel name')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    sp_list.add_argument('--long', action='store_true', help='in long format')

def sw2_channel_list(args, env):
    headers = { 'Cache-Control': 'no-cache' }
    options = []
    if args.name:
        options.append('='.join(['name', args.name]))
    if args.strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([env.apiChannels(), '&'.join(options)])

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    channels = json.loads(res.text)
    for channel in channels:
        if args.long:
            print(args.delimiter[0].join([str(channel["id"]), channel["name"], str(channel["enabled"]), channel["created"], channel["updated"]]))
        else:
            print(args.delimiter[0].join([str(channel["id"]), channel["name"]]))

    return 0