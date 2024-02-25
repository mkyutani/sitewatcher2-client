import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment

def unset_directory_variables(id, key):
    headers = {}

    if key is not None:
        key_path = f'?key={key}'
    else:
        key_path = ''

    query = urljoin(Environment().apiSites(), f'{id}/metadata{key_path}')

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    return []