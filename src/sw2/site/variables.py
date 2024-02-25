import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment

def get_site_variables(id, key=None):
    headers = { 'Cache-Control': 'no-cache' }

    if key is not None:
        key_path = f'?key={key}'
    else:
        key_path = ''

    query = urljoin(Environment().apiSites(), f'{id}/metadata{key_path}')

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    metadata = json.loads(res.text)

    return metadata