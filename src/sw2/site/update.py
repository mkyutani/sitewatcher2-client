import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.site.link_list import get_list_links
from sw2.site.list import get_site_resources, get_sites

from sw2.env import Environment

def push_site_resource(site, link, name, sections, reason, initial=False):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': link,
        'name': name,
        'sections': sections,
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

    return resource

def update_site_resources(site, push=False, initial=False):
    if type(site) is dict:
        pass
    else:
        site = get_sites(site, single=True)
        if site is None:
            return None

    resource_dict = {}
    resources = get_site_resources(site['id'])
    if resources is not None:
        for resource in resources:
            resource_dict[resource['uri']] = resource

    messages = []

    links = get_list_links(site['uri'])
    excludes = [kv['value'] for kv in site['metadata'] if kv['key'] == 'exclude']
    unique_uris = []
    for link in links:
        message = ' '.join([link['uri'], link['name'] if link['section'] is None else f'{link["section"]}::{link["name"]}'])
        op = ' '
        for exclude in excludes:
            if re.match(exclude, link['uri']):
                op = 'X'
                break
        else:
            if link['uri'] in unique_uris:
                op = '='
            else:
                unique_uris.append(link['uri'])
                if resource_dict.pop(link['uri'], None) is None:
                    op = '+'
                    if push:
                        push_site_resource(site['id'], link['uri'], link['name'], link['sections'], "new", initial=initial)

        messages.append({
            'message': message,
            'op': op,
            **link,
            'site': site['id'],
            'site_name': site['name'],
            'site_uri': site['uri'],
            'directory': site['directory'],
            'directory_name': site['directory_name']
        })

    for resource in resource_dict.values():
        message = ' '.join([resource['uri'], resource['name']])
        messages.append({
            'message': message,
            'op': '-',
            **resource,
            'site': site['id'],
            'site_name': site['name'],
            'site_uri': site['uri'],
            'directory': site['directory'],
            'directory_name': site['directory_name']
        })

    return messages