import feedparser
import os
import re
import sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

from sw2.util import to_printable

def get_rss_links(source):
    feed = None
    try:
        feed = feedparser.parse(source)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return []

    links = []
    for e in feed['entries']:
        links.append({
            'uri': e['link'],
            'name': e['title'],
            'properties': {
                '_uri': e['link'],
                '_name': e['title'],
            }
        })

    return links

class Tag:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

def interpret_html_walk_expression(html_walk_expression):
    ops = []

    expr = html_walk_expression
    while True:
        if len(expr) == 0:
            return ops
        elif expr[0] in '0123456789':
            num = 0
            while len(expr) > 0 and expr[0] in '0123456789':
                num = num * 10 + int(expr[0])
                expr = expr[1:]
            ops.append(num)
        elif expr[0] in '^.<>':
            ops.append(expr[0])
            expr = expr[1:]
        elif expr[0] in ' ,':
            pass
        elif expr[0] == '[':
            tag_name = ''
            expr = expr[1:]
            while len(expr) > 0 and expr[0] != ']':
                tag_name = tag_name + expr[0]
                expr = expr[1:]
            ops.append(Tag(tag_name))
        else:
            ops.append(expr[0])
            expr = expr[1:]

def walk(source_uri, soup, html_walk_expression, regular_expression):
    content = None
    footprints = []

    ops = interpret_html_walk_expression(html_walk_expression)
    tag = soup
    footprints.append(tag.name if tag.name else '?')
    for op in ops:
        if type(op) == Tag:
            searched = None
            if hasattr(tag, 'siblings')and tag.siblings:
                for t in tag.siblings:
                    if t.name == op.name:
                        searched = t
                        break
            if not searched and hasattr(tag, 'parents') and tag.parents:
                for t in tag.parents:
                    if t.name == op.name:
                        searched = t
                        break
            if searched is None:
                tag = None
                footprints.append('*')
            else:
                tag = searched
                footprints.append(tag.name if tag.name else '?')
        elif type(op) == int:
            found = None
            index = op
            if hasattr(tag, 'children') and tag.children:
                for t in tag.children:
                    if index == 0:
                        found = t
                        break
                    index = index - 1
            if found is None:
                footprints.append('*')
            else:
                tag = found
                footprints.append(tag.name if tag.name else '?')
        elif op == '^':
            found = None
            if hasattr(tag, 'parent') and tag.parent:
                found = tag.parent
            if found is None:
                footprints.append('*')
            else:
                tag = found
                footprints.append(tag.name if tag.name else '?')
        elif op == '.':
            found = None
            if hasattr(tag, 'children'):
                for t in tag.children:
                    if found is None:
                        found = t
                        break
                    break
            if found is None:
                footprints.append('*')
            else:
                tag = found
                footprints.append(tag.name if tag.name else '?')
        elif op == '<':
            found = None
            if hasattr(tag, 'previous_sibling') and tag.previous_sibling:
                found = tag.previous_sibling
                footprints.append(tag.name if tag.name else '?')
            else:
                footprints.append('*')
        elif op == '>':
            found = None
            if hasattr(tag, 'next_sibling') and tag.next_sibling:
                found = tag.next_sibling
                footprints.append(tag.name if tag.name else '?')
            else:
                footprints.append('*')
        else:
            footprints.append('*')
            continue

        if tag is None:
            footprints.append('None')
            break

        if hasattr(tag, 'name') and tag.name:
            if content is None:
                content = ''
            else:
                content = content + '::'
            content = content + tag.name

    if tag is None:
        return None

    text = ''.join(filter(lambda c: c >= ' ', tag.text.strip()))

    if len(text) > 0:
        if content is None:
            content = text
        else:
            content = content + '::' + text

    if content and regular_expression:
        sep = regular_expression[0]
        operands = regular_expression[1:].split(sep)
        if len(operands) < 2 or len(operands) > 3:
            print(f'Invalid property template value (html_walk_expression)', file=sys.stderr)
        else:
            pattern = operands[0]
            compiled_pattern = re.compile(pattern)
            if len(operands) == 2:
                matched = re.search(compiled_pattern, content)
                if matched:
                    content = matched.group()
            else:
                replaced = operands[1]
                matched, count = re.subn(compiled_pattern, replaced, content)
                if count > 0 and matched:
                    content = matched

    all_footprints = ','.join(footprints)
    print(f'{os.path.basename(source_uri)}:{all_footprints}:{content}', file=sys.stderr)

    return content

def get_html_links(source, html_walk_expression = None):
    headers = { 'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' }
    property_value_max = 4096

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
            section_text = tag.text.strip()
            section_text = re.sub('<.*?>', '', section_text)
            sections[level - 1] = section_text
            for i in range(level, 6):
                sections[i] = None
        elif tag.name == 'title':
            title = tag.text.strip()
        elif tag.name == 'table':
            table_header = None
        elif tag.name =='tr':
            if table_header is None:
                for th in tag.find_all('th'):
                    found = th.text.strip()
                    if len(found) > 0:
                        if table_header is None:
                            table_header = ''
                        else:
                            table_header = table_header + '::'
                        table_header = table_header + found
        else:
            table_rows = None
            list_items = None
            definition_term = None
            walk_contents = {}
            for anc in tag.parents:
                if anc.name == 'li' and list_items is None:
                    tag_text_list = list(filter(lambda x: len(x) > 0, [s.strip() for s in anc.strings]))
                    if len(tag_text_list) > 0:
                        list_items = '::'.join(tag_text_list)
                elif anc.name == 'tr' and table_rows is None:
                    tag_text_list = list(filter(lambda x: len(x) > 0, [s.strip() for s in anc.strings]))
                    if len(tag_text_list) > 0:
                        table_rows = '::'.join(tag_text_list)
                elif anc.name == 'dl' and definition_term is None:
                    for dt in anc.find_all('dt'):
                        found = dt.text.strip()
                        if len(found) > 0:
                            if definition_term is None:
                                definition_term = ''
                            else:
                                definition_term = definition_term + '::'
                            definition_term = definition_term + found

            if html_walk_expression is not None:
                for rule in html_walk_expression:
                    value = walk(source, tag, rule['src'], rule['value'])
                    if value is not None:
                        walk_contents.update({rule['dst']: value})

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

            href = tag.get('href')
            if href is not None:
                ref = href.strip()
                ref = re.sub('<.*?>', '', ref)
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
                    name = tag_text
                    name = ''.join(filter(lambda c: c >= ' ', name))
                    name = re.sub('\s', '_', name)
                    if len(name) == 0:
                        name = 'No name'

                    properties = {}
                    properties['_uri'] = uri
                    properties['_name'] = name
                    if title is not None:
                        title = to_printable(title)
                        properties['_title'] = title[:property_value_max]
                    if table_header is not None:
                        table_header = to_printable(table_header)
                        properties['_th'] = table_header[:property_value_max]
                    if table_rows is not None:
                        table_rows = to_printable(table_rows)
                        properties['_tr'] = table_rows[:property_value_max]
                    if list_items is not None:
                        list_items = to_printable(list_items)
                        properties['_li'] = list_items[:property_value_max]
                    if definition_term is not None:
                        definition_term = to_printable(definition_term)
                        properties['_dt'] = definition_term[:property_value_max]
                    for i in range(6):
                        if sections[i] is not None:
                            section_text = to_printable(sections[i])
                            properties[f'_h{i + 1}'] = section_text[:property_value_max]
                    for key in walk_contents:
                        property = to_printable(walk_contents[key])
                        properties[key] = property[:property_value_max]
                    if len(ancestors_text) > 0:
                        ancestors = to_printable(ancestors_text)
                        properties['_tags'] = ancestors[:property_value_max]

                    links.append({
                        'uri': uri,
                        'name': name,
                        'properties': properties
                    })

    return links

def get_list_links(source, link_list_rules = None):
    source_type = None
    source_uri = source

    source_lower = source.lower()
    if source_lower.startswith('rss:'):
        source_type = 'rss'
        source_uri = source[4:]
    elif source_lower.startswith('html:'):
        source_uri = source[5:]
    elif source_lower.endswith('.rss') or source_lower.endswith('.rdf') or source_lower.endswith('.xml'):
        source_type = 'rss'

    if source_type == 'rss':
        return get_rss_links(source_uri)
    else:
        return get_html_links(source_uri, html_walk_expression = link_list_rules)
