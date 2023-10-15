import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_directory_status(subparser):
    sp_list = subparser.add_parser('status', help='get task status')
    sp_list.add_argument('target', metavar='TARGET', default=None, help='directory id')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    sp_list.add_argument('--long', action='store_true', help='in long format')

def sw2_directory_status(args, env):
    headers = { 'Cache-Control': 'no-cache' }
    options = []
    if args.target:
        options.append('='.join(['target', args.target]))
    query = '?'.join([env.apiDirectoryCollectors(), '&'.join(options)])
    print(query, file=sys.stderr)

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

    directoryCollector = json.loads(res.text)
    if args.long:
        print(args.delimiter[0].join([str(directoryCollector["id"]), directoryCollector["target"], directoryCollector["status"], directoryCollector["created"], directoryCollector["updated"]]))
    else:
        print(args.delimiter[0].join([str(directoryCollector["id"]), directoryCollector["status"]]))

    return 0