import json
import json
import re
import requests
import sys
from sw2.env import Environment

from sw2.directory.sites import get_sites_by_directory
from sw2.site.link_list import get_list_links
from sw2.site.resource import get_site_resources

def update_directory_resources(directory_id):

    sites = get_sites_by_directory(directory_id)
    for site in sites:
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
            messages.append({
                'message': message,
                'op': op,
                **link,
                'site': site['id'],
                'site_name': site['name'],
                'site_uri': site['uri'],
                'directory': directory_id,
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
                'directory': directory_id,
                'directory_name': site['directory_name']
            })

    return messages