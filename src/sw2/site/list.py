import json
import json
import re
from urllib.parse import urljoin
import requests
import sys
from sw2.env import Environment
from sw2.util import is_uuid

def get_site(id):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiSites() + id

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

    site = json.loads(res.text)
    return site

def list_sites(name, strict=False):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiSites()

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

    site_id_names = json.loads(res.text)

    if name is None or name.lower() == 'all':
        return site_id_names
    else:
        target_id_names = []
        for site_id_name in site_id_names:
            if strict:
                if name == site_id_name['name']:
                    target_id_names.append(site_id_name)
            else:
                if re.search(name, site_id_name['name']):
                    target_id_names.append(site_id_name)
        return target_id_names

def get_sites(name, strict=False):
    sites = []
    if name and is_uuid(name):
        site = get_site(name)
        if site is None:
            return None
        else:
            sites.append(site)
    else:
        sites = []
        directory_id_names = list_sites(name, strict=strict)
        for id_name in directory_id_names:
            site = get_site(id_name['id'])
            if site is None:
                return None
            else:
                sites.append(site)

    return sites

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