import json
import sys
from urllib.parse import urljoin
import requests

def sw2_parser_collect(subparser):
    sp_list = subparser.add_parser('collect', help='collect site resources')
    sp_list.add_argument('id', metavar='ID', help='id')

def sw2_collect(args, env):
    headers = {}
    query = urljoin(env.apiSites(), args.id) + '/resources'

    res = None
    try:
        res = requests.put(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'Response {message} ', file=sys.stderr)
        return 1

    count = json.loads(res.text)
    if 'count' in count:
        count = count['count']
        print(count)

    return 0