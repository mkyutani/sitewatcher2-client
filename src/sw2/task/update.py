import json
import re
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment
from sw2.site.func_resources import get_site_resources
from sw2.task.list_links import get_list_links
from sw2.task.site_structure import get_site_structure

def sw2_parser_task_update(subparser):
    parser = subparser.add_parser('update', help='update site links')
    parser.add_argument('directory', nargs=1, help='directory id, name, "all"')
    parser.add_argument('site', nargs='?', default=None, help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def push(site, link, reason):
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

def update_sites(sites, do_push=False, all=False):
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
            for exclude in excludes:
                if re.match(exclude, link['uri']):
                    messages.append({'message': message, 'op': 'S'})
                    break
            else:
                if link['uri'] in unique_uris:
                    messages.append({'message': message, 'op': 'D'})
                else:
                    unique_uris.append(link['uri'])
                    if resource_dict.pop(link['uri'], None) is None:
                        if do_push:
                            push(site, link, "new")
                        messages.append({'message': message, 'op': '+'})
                    else:
                        messages.append({'message': message, 'op': ' '})
        for resource in resource_dict.values():
            message = ' '.join([resource['uri'], resource['name']])
            messages.append({'message': message, 'op': '-'})

        for message in messages:
            if all or message['op'] in '+-':
                print(message['op'], message['message'])

def sw2_task_update(args):
    args_directory = args.get('directory')[0]
    args_site = args.get('site')[0] if args.get('site') else None
    args_all = args.get('all')
    args_strict = args.get('strict')
    args_push = args.get('push')

    sites = get_site_structure(args_directory, args_site, strict=args_strict, all=args_all)
    if sites is None:
        return 1

    if len(sites) == 0:
        print(f'No such a site', file=sys.stderr)
        return 1

    update_sites(sites, do_push=args_push, all=args_all)

    return 0