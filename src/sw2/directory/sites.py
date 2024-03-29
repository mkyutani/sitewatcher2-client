import json
import json
import requests
import sys
from sw2.env import Environment

def get_sites_by_directory(directory_id):
    headers = { 'Cache-Control': 'no-cache' }
    query = f'{Environment().apiDirectories()}{directory_id}/sites'

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return []

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return []

    return json.loads(res.text)