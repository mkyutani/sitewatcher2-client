import json
import re
import sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from sw2.env import Environment
from sw2.site.list import get_sites_by_directory_and_site_name
from sw2.site.resources import get_site_resources

def sw2_parser_task_list(subparser):
    parser = subparser.add_parser('list', help='list links')
    parser.add_argument('directory', nargs=1, help='directory id, name, "all" or "test:url"')
    parser.add_argument('site', nargs='?', default=None, help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

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
        parent_tag_text = ''
        for anc in a.parents:
            if anc.name == 'li' or anc.name == 'tr':
                tag_texts = list(filter(lambda x: len(x) > 0, [s.strip() for s in anc.strings]))
                if len(tag_texts) > 1:
                    parent_tag_text = tag_texts[0].strip()
                break
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

                tag_text = a.text.strip()
                if tag_text is None:
                    tag_text = ''
                if tag_text == parent_tag_text:
                    parent_tag_text = ''
                name = parent_tag_text + '::' + tag_text if len(parent_tag_text) > 0 else tag_text
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
    args_directory = args.get('directory')[0]
    args_site = args.get('site')[0] if args.get('site') else None
    args_all = args.get('all')
    args_strict = args.get('strict')
    args_push = args.get('push')

    if args_directory.lower().startswith('test:'):
        links = get_list_links(args_directory[5:])
        for link in links:
            print(link['uri'], link['name'])
        return 0

    sites = get_sites_by_directory_and_site_name(args_directory, args_site, args_strict, args_all)
    if sites is None:
        return 1

    if len(sites) == 0:
        print(f'No such a site', file=sys.stderr)
        return 1

    for site in sites:
        resource_dict = {}
        resources = get_site_resources(site['id'])
        if resources is not None:
            for resource in resources:
                resource_dict[resource['uri']] = resource

        messages = []

        links = get_list_links(site['uri'])
        unique_uris = []
        for link in links:
            message = ' '.join([link['uri'], link['name']])
            if link['uri'] in unique_uris:
                messages.append({'message': message, 'op': ' '})
            else:
                unique_uris.append(link['uri'])
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
            if args_all or message['op'] != ' ':
                print(message['op'], message['message'])

    return 0