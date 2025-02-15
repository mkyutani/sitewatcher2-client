import json
import json
import re
from urllib.parse import urljoin
import requests
import sys
from sw2.directory.list import get_directory, list_directories
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
            directory_name, site_name = name.split(':', 1)
            if len(directory_name) == 0:
                directory_name = None
            if len(site_name) == 0:
                site_name = None

            directory_id_names = list_directories(directory_name, strict=strict)
            if directory_id_names is None:
                return None

            for directory_id_name in directory_id_names:
                directory = get_directory(directory_id_name['id'])
                if directory:
                    for site in directory['sites']:
                        site.update({
                            'directory': {
                                'id': directory['id'],
                                'name': directory['name'],
                                'created': directory['created'],
                                'updated': directory['updated'],
                                'rule_category_names': directory['rule_category_names']
                            }
                        })
                        del site['directory_name']
                        for rule_category_name in directory['rule_category_names']:
                            site['directory'][rule_category_name] = directory[rule_category_name]

                        if site_name is None or site_name.lower() == 'all':
                            sites.append(site)
                        elif strict:
                            if site_name == site['name']:
                                sites.append(site)
                        else:
                            if site_name is None or re.search(site_name, site['name']):
                                sites.append(site)

        else:
            site_id_names = list_sites(name, strict=strict)
            if site_id_names is None:
                return None

            for id_name in site_id_names:
                site = get_site(id_name['id'])
                if site is None:
                    return None
                else:
                    sites.append(site)

    if len(sites) == 0:
        return None

    return sites