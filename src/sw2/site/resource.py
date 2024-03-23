import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment

def get_site_resources(id):
    query = urljoin(Environment().apiSites(), f'{id}/resources')

    res = None
    try:
        res = requests.get(query)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    resources = json.loads(res.text)
    return resources

def push_site_resource(site, link, name, reason, initial=False):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': link,
        'name': name,
        'reason': reason,
    }
    options = []
    if initial:
        options.append('initial')

    query = '?'.join([urljoin(Environment().apiSites(), f'{site}/resources'), '&'.join(options)])

    res = None
    try:
        res = requests.post(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    resource = json.loads(res.text)