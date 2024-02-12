import json
import re
import sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, NavigableString

def sw2_parser_task_list(subparser):
    sp_list = subparser.add_parser('list', help='list links')
    sp_list.add_argument('name', nargs='?', metavar='NAME', default=None, help='site name')
    sp_list.add_argument('--strict', action='store_true', help='strict name check')
    sp_list.add_argument('--push', action='store_true', help='push to remote')
    sp_list.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')

def get_list_links(source) -> list[str]:
    headers = { 'Cache-Control': 'no-cache' }
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

def sw2_task_list(args, env):
    headers = { 'Cache-Control': 'no-cache' }
    options = [ 'enabled=true' ]
    if args.name:
        options.append('='.join(['name', args.name]))
    if args.strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([env.apiSites(), '&'.join(options)])

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    sites = json.loads(res.text)
    for site in sites:
        links = get_list_links(site['uri'])
        for link in links:
            print(link['uri'], link['name'], sep=args.delimiter[0])

    return 0