import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.site.link_list import get_list_links
from sw2.site.list import get_sites
from sw2.env import Environment

def push_resource(site, uri, properties):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': uri,
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

    if res.status_code == 204:
        return None
    else:
        resource = json.loads(res.text)
        return resource

def test_resource_by_rules(site, link):
    if site.get('rule_category_names') is None:
        return False, 'No rules in site structure'

    excludes = site.get('exclude')
    if excludes is not None:
        excludes.sort(key=lambda x: x.get('weight', 0))
        for exclude in excludes:
            condition = exclude['value']
            property_name, pattern = condition.split(':', 1)
            property_text = link['properties'].get(property_name)
            if property_text is not None and re.search(pattern, property_text):
                return False, f'{link["name"]} ({property_name}:{property_text}) excluded by rule [{condition}]'

    includes = site.get('include')
    if includes is not None:
        includes.sort(key=lambda x: x.get('weight', 0))
        for include in includes:
            condition = include['value']
            property_name, pattern = condition.split(':', 1)
            property_text = link['properties'].get(property_name)
            if property_text is not None and re.search(pattern, property_text):
                break
        else:
            return False, f'{link["name"]} not included'

    return True, None

def test_resources(site):
    links = get_list_links(site['uri'])

    resources = []
    for link in links:
        result, reason = test_resource_by_rules(site, link)
        if result:
            resources.append(link)
        else:
            print(reason, file=sys.stderr)

    return resources

def update_resources(site):
    links = get_list_links(site['uri'])

    resources = []
    for link in links:
        result, reason = test_resource_by_rules(site, link)
        if result:
            resource = push_resource(site['id'], link['uri'], link['properties'])
            if resource is not None:
                resources.append(resource)
        else:
            print(reason, file=sys.stderr)

    return resources

def get_resources(id):
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