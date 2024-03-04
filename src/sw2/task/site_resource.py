import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment

def push_site_resource(site, link, reason):
    site_id = site['id']
    site_name = site['name']
    link_uri = link['uri']
    link_name = link['name']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': link_uri,
        'name': link_name,
        'reason': reason,
    }

    query = urljoin(Environment().apiSites(), f'{site_id}/resources')

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