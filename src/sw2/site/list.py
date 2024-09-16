import json
import json
import re
from urllib.parse import urljoin
import requests
import sys
from sw2.directory.list import list_directories
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
        if name and name.find(':') >= 0:
            directory_name, site_name = name.split(':')

            if len(directory_name) == 0:
                directory_name = None
            directory_id_names = list_directories(directory_name, strict=strict)
            if directory_id_names is None:
                return None

            if len(site_name) == 0:
                site_name = None
            site_id_names = list_sites(site_name, strict=strict)
            if site_id_names is None:
                return None

            sites = []
            for site_id_name in site_id_names:
                site = get_site(site_id_name['id'])
                if site is None:
                    pass
                elif directory_id_names is not None:
                    for directory_id_name in directory_id_names:
                        if site['directory']['id'] == directory_id_name['id']:
                            sites.append(site)
                else:
                    sites.append(site)
            if len(sites) == 0:
                return None
        else:
            sites = []
            site_id_names = list_sites(name, strict=strict)
            if site_id_names is None:
                return None
            for id_name in site_id_names:
                site = get_site(id_name['id'])
                if site is None:
                    return None
                else:
                    sites.append(site)

    return sites