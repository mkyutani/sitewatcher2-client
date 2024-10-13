import copy
import re
import sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

def get_list_links(source):
    headers = { 'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' }

    try:
        res = requests.get(source, headers=headers, timeout=10)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return []

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
    sections = [None] * 6
    title = None
    table_header = None
    name = None
    for tag in bs.find_all(['title', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'tr']):
        if tag.name[0] == 'h':
            level = int(tag.name[1])
            section_text = ''.join(filter(lambda c: c >= ' ', tag.text.strip()))
            section_text = re.sub('<.*?>', '', section_text)
            sections[level - 1] = section_text
            for i in range(level, 6):
                sections[i] = None
        elif tag.name == 'title':
            title = ''.join(filter(lambda c: c >= ' ', tag.text.strip()))
        elif tag.name == 'table':
            table_header = None
        elif tag.name =='tr':
            if table_header is None:
                for th in tag.find_all('th'):
                    found = ''.join(filter(lambda c: c >= ' ', th.text.strip()))
                    if table_header is None:
                        table_header = ''
                    else:
                        table_header = table_header + '::'
                    table_header = table_header + found
        else:
            parent_tag_text = None
            for anc in tag.parents:
                if (anc.name == 'li' and parent_tag_text is None) or anc.name == 'tr':
                    tag_texts = list(filter(lambda x: len(x) > 0, [s.strip() for s in anc.strings]))
                    if len(tag_texts) > 1:
                        tag_first = tag_texts[0].strip()
                        if tag_first and len(tag_first) > 0:
                            parent_tag_text = tag_first
                            if anc.name == 'tr':
                                break

            ancestors = []
            for anc in tag.parents:
                if anc.name == 'document' or anc.name == 'html' or anc.name == 'body':
                    break
                attrs = []
                for key in anc.attrs:
                    if key == 'id' or key == 'class':
                        if type(anc[key]) == list:
                            attrs.append(f'{key}={",".join(anc[key])}')
                        else:
                            attrs.append(f'{key}={anc[key]}')
                if len(attrs) > 0:
                    attrs_string = ','.join(attrs)
                else:
                    attrs_string = None
                if anc.contents is None or anc.contents[0] is None or anc.contents[0].text is None:
                    text = None
                else:
                    text = ''.join([c.text.strip() for c in anc.contents if c.name is None])
                    if len(text) == 0:
                        text = None
                ancestor_text = ':'.join(list(filter(lambda x: x is not None, [anc.name, attrs_string, text])))
                ancestors.append(ancestor_text)
            ancestors.reverse()
            ancestors_text = ';'.join(ancestors)

            if parent_tag_text is None:
                parent_tag_text = ''
            href = tag.get('href')
            if href is not None:
                ref = ''.join(filter(lambda c: c >= ' ', href))
                ref = re.sub('<.*?>', '', ref)
                ref = ref.strip()
                if not (ref.startswith('#') or ref.startswith('mailto:') or ref.startswith('tel:') or ref.startswith('javascript:')):
                    if re.match(r'^[^:]*:', ref):
                        uri = ref
                    elif re.match(r'^\/\/', ref):
                        uri = f'{source_url_base.scheme}:{ref}'
                    elif re.match(r'^/', ref):
                        uri = f'{source_url_base.scheme}://{source_url_base.netloc}{ref}'
                    else:
                        uri = urljoin(source, ref)

                    tag_text = tag.text.strip()
                    if tag_text is None:
                        tag_text = ''
                    if tag_text == parent_tag_text:
                        parent_tag_text = ''
                    name = parent_tag_text + '::' + tag_text if len(parent_tag_text) > 0 else tag_text
                    name = ''.join(filter(lambda c: c >= ' ', name))
                    name = re.sub('\s', '_', name)
                    if len(name) == 0:
                        name = 'No name'

                    properties = {}
                    properties['_uri'] = uri
                    properties['_name'] = name
                    if title is not None:
                        properties['_title'] = title
                    if table_header is not None:
                        properties['_th'] = table_header
                    for i in range(6):
                        if sections[i] is not None:
                            properties[f'_h{i + 1}'] = sections[i]
                    if len(ancestors_text) > 0:
                        properties['_tags'] = ancestors_text

                    links.append({
                        'uri': uri,
                        'name': name,
                        'properties': properties
                    })

    return links