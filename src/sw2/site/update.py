import json
import sys
from urllib.parse import urljoin
import requests

from sw2.site.link_list import get_list_links
from sw2.site.list import get_sites
from sw2.env import Environment

def push_site_resource(site, uri, name, properties):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': uri,
        'name': name,
        'properties': properties
    }

    query = urljoin(Environment().apiSites(), f'{site}/resources')

    res = None
    try:
        res = requests.post(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    resource = json.loads(res.text)

    return resource

def update_site_resources(site, push=False):
    if type(site) is not dict:
        site = get_sites(site, single=True)
        if site is None:
            return None

    links = get_list_links(site['uri'])
    if not push:
        return links
    else:
        resources = []
        for link in links:
            resource = push_site_resource(site['id'], link['uri'], link['name'], link['properties'])
            if resource is not None:
                resources.append(resource)
        return resources