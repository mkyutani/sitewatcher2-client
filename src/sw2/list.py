import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def func_list(args):

    env = Environment()

    api_base = urljoin(env.server(), "/api/v1/sites")

    res = None
    headers = { 'Cache-Control': 'no-cache' }

    options = []
    if args.name:
        options.append('='.join(['name', args.name]))
    if args.strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([api_base, '&'.join(options)])

    try:
        res = requests.get(query, headers=headers)
    except requests.exceptions.RequestException as e:
        print('Failed to fetch', file=sys.stderr)
        return None
    except Exception as e:
        print('Failed to fetch', file=sys.stderr)
        return None

    if res.status_code == 403:
        try:
            headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' })
            res = requests.get(api_base, headers=headers)
        except requests.exceptions.RequestException as e:
            print('Failed to fetch', file=sys.stderr)
            return None
        except Exception as e:
            print('Failed to fetch', file=sys.stderr)
            return None
    elif res.status_code >= 400:
        print('Failed to fetch ({})'.format(res.status_code), file=sys.stderr)
        return None

    sites = json.loads(res.text)
    for site in sites:
        if args.long:
            print(args.delimiter[0].join([str(site["id"]), site["name"], site["uri"], site["type"], str(site["enabled"]), site["lastupdated"]]))
        else:
            print(args.delimiter[0].join([str(site["id"]), site["name"], site["uri"]]))
