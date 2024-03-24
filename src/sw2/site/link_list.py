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
    for tag in bs.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if tag.name[0] == 'h':
            level = int(tag.name[1])
            section_text = ''.join(filter(lambda c: c >= ' ', tag.text.strip()))
            section_text = re.sub('<.*?>', '', section_text)
            sections[level - 1] = section_text
            for i in range(level, 6):
                sections[i] = None
        else:
            parent_tag_text = ''
            for anc in tag.parents:
                if anc.name == 'li' or anc.name == 'tr':
                    tag_texts = list(filter(lambda x: len(x) > 0, [s.strip() for s in anc.strings]))
                    if len(tag_texts) > 1:
                        parent_tag_text = tag_texts[0].strip()
                    break
            href = tag.get('href')
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

                    tag_text = tag.text.strip()
                    if tag_text is None:
                        tag_text = ''
                    if tag_text == parent_tag_text:
                        parent_tag_text = ''
                    name = parent_tag_text + ':' + tag_text if len(parent_tag_text) > 0 else tag_text
                    name = ''.join(filter(lambda c: c >= ' ', name))
                    if len(name) == 0:
                        name = '----'

                    links.append({
                        'sections': copy.deepcopy(sections),
                        'section': ':'.join(list(map(lambda x: x if x is not None else '', sections))),
                        'uri': uri,
                        'name': name
                    })

    return links