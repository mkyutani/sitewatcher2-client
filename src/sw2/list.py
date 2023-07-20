import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def func_list(args):

    env = Environment()

    api_base = urljoin(env.server(), "/api/v1/sites")

    res = None
    headers = { 'Cache-Control': 'no-cache' }

    delim = '?'
    query = api_base
    if args.name:
        query =  f'{query}{delim}name={args.name}'
        delim = '&'
    if args.strict:
        query = f'{query}{delim}strict=true'

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

    print(res.text)
