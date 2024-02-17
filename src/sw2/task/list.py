import json
import re
import sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from sw2.directory.list import get_directories_by_name
from sw2.directory.sites import get_sites_by_directory
from sw2.env import Environment
from sw2.site.list import get_sites_by_name
from sw2.site.resources import get_site_resources

def sw2_parser_task_list(subparser):
    sp_list = subparser.add_parser('list', help='list links')
    target_group = sp_list.add_mutually_exclusive_group()
    target_group.add_argument('--name', nargs=1, metavar='NAME', help='site name')
    target_group.add_argument('--directory', nargs=1, help='directory name')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')
    sp_list.add_argument('--push', action='store_true', help='push to remote')

def get_list_links(source):
    headers = { 'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' }
    res = requests.get(source, headers=headers)
    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return []

    if not 'Content-Type' in res.headers:
        print('No Content-Type', file=sys.stderr)
        return []

    content_type_fragments = res.headers['Content-Type'].split(';')

    mime_type = content_type_fragments[0].strip().lower()
    if mime_type != 'text/html':
        print(f'Unexpected mime type {mime_type}', file=sys.stderr)
        return []

    if len(content_type_fragments) < 2:
        print(f'Warning: No charset; assume utf-8', file=sys.stderr)
    else:
        charset = content_type_fragments[1].split('=')[1].strip().lower()
        if charset != 'utf-8':
            print(f'Unexpected charset {charset}', file=sys.stderr)
            return []

    if len(res.text) == 0:
        print('Empty content', file=sys.stderr)
        return []

    source_url_base = urlparse(source)
    links = []

    bs = BeautifulSoup(res.content, 'html.parser')
    for a in bs.find_all('a'):
        href = a.get('href')
        if href is not None:
            ref = ''.join(filter(lambda c: c >= ' ', href))
            ref = re.sub('<.*?>', '', ref)
            ref = ref.strip().lower()
            if not (ref.startswith('#') or ref.startswith('mailto:') or ref.startswith('tel:') or ref.startswith('javascript:')):
                if re.match(r'^[^:]*:', ref):
                    uri = ref
                elif re.match(r'^\/\/', ref):
                    uri = f'{source_url_base.scheme}:{ref}'
                elif re.match(r'^/', ref):
                    uri = f'{source_url_base.scheme}://{source_url_base.netloc}{ref}'
                else:
                    uri = urljoin(source, ref)

                name = ''
                name_strings = a.strings
                if name_strings is not None:
                    name = '::'.join(filter(lambda x: len(x) > 0, [s.strip() for s in name_strings]))
                    name = ''.join(filter(lambda c: c >= ' ', name))
                if len(name) == 0:
                    name = '----'

                links.append({
                    'uri': uri,
                    'name': name
                })

    return links

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

def sw2_task_list(args):
    args_name = args.get('name')
    args_directory = args.get('directory')
    args_strict = args.get('strict')
    args_push = args.get('push')

    if args_name is not None:
        sites = get_sites_by_name(args_name[0], args_strict)
    elif args_directory is not None:
        directories = get_directories_by_name(args_directory[0], args_strict)
        for directory in directories:
            sites = get_sites_by_directory(directory['id'])
    else:
        print('name or directory must be specified', file=sys.stderr)
        return 1

    if len(sites) == 0:
        print(f'No such a site', file=sys.stderr)
        return 1

    for site in sites:
        resources = get_site_resources(site['id'])
        resource_dict = {}
        for resource in resources:
            resource_dict[resource['uri']] = resource

        messages = []

        print(f'{site["name"]} ({site["uri"]})', file=sys.stderr)
        links = get_list_links(site['uri'])
        for link in links:
            message = ' '.join([link['uri'], link['name']])
            if args_push:
                if resource_dict.pop(link['uri'], None) is None:
                    push(site, link, "new")
                    messages.append({'message': message, 'op': '+'})
            else:
                if resource_dict.pop(link['uri'], None) is None:
                    messages.append({'message': message, 'op': '+'})
                else:
                    messages.append({'message': message, 'op': ' '})
        if not args_push:
            for resource in resource_dict.values():
                message = ' '.join([resource['uri'], resource['name']])
                messages.append({'message': message, 'op': '-'})

        messages.sort(key=lambda x: x['message'])
        for message in messages:
            print(message['op'], message['message'])

    return 0