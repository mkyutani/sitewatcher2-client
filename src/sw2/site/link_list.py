import feedparser
import hashlib
import re
import sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

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
        else:
            ops.append(expr[0])
            expr = expr[1:]

def walk(soup, html_walk_expression, regular_expression):
    content = None

    ops = interpret_html_walk_expression(html_walk_expression)
    tag = soup
    searched = None
    for op in ops:
        if type(op) == int:
            index = op
            for t in tag.children:
                if index == 0:
                    tag = t
                    break
                index = index - 1
        elif op == '^':
            tag = tag.parent
        elif op == '.':
            for t in tag.children:
                tag = t
                break
        elif op == '<':
            tag = tag.previous_sibling
        elif op == '>':
            tag = tag.next_sibling
        elif op == ' ':
            pass

        if tag is None:
            break

        if tag.name is not None:
            if content is None:
                content = ''
            else:
                content = content + '::'
            content = content + tag.name

    if tag is None:
        return None

    if searched is not None:
        text = searched
    else:
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
                        found = ''.join(filter(lambda c: c >= ' ', dt.text.strip()))
                        if len(found) > 0:
                            if definition_term is None:
                                definition_term = ''
                            else:
                                definition_term = definition_term + '::'
                            definition_term = definition_term + found

            if html_walk_expression is not None:
                for rule in html_walk_expression:
                    value = walk(tag, rule['src'], rule['value'])
                    if value is not None:
                        walk_contents.update({rule['dst']: value})

            previous = None
            previous_tag_text_list = []
            for anc in tag.previous_siblings:
                if anc.name == 'a':
                    break
                previous_tag_text_list.append(''.join(list(filter(lambda c: c >= ' ', anc.text.strip()))))
                if len(previous_tag_text_list) > 0:
                    previous = '::'.join(list(filter(lambda x: len(x) > 0, previous_tag_text_list)))

            next = None
            next_tag_text_list = []
            for anc in tag.next_siblings:
                if anc.name == 'a':
                    break
                next_tag_text_list.append(''.join(list(filter(lambda c: c >= ' ', anc.text.strip()))))
                if len(next_tag_text_list) > 0:
                    next = '::'.join(list(filter(lambda x: len(x) > 0, next_tag_text_list)))

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
                    name = tag_text
                    name = ''.join(filter(lambda c: c >= ' ', name))
                    name = re.sub('\s', '_', name)
                    if len(name) == 0:
                        name = 'No name'

                    properties = {}
                    properties['_uri'] = uri
                    properties['_name'] = name
                    if title is not None:
                        properties['_title'] = title[:property_value_max]
                    if table_header is not None:
                        properties['_th'] = table_header[:property_value_max]
                    if table_rows is not None:
                        properties['_tr'] = table_rows[:property_value_max]
                    if list_items is not None:
                        properties['_li'] = list_items[:property_value_max]
                    if definition_term is not None:
                        properties['_dt'] = definition_term[:property_value_max]
                    if previous is not None:
                        properties['_prev'] = previous[:property_value_max]
                    if next is not None:
                        properties['_next'] = next[:property_value_max]
                    for i in range(6):
                        if sections[i] is not None:
                            properties[f'_h{i + 1}'] = sections[i][:property_value_max]
                    for key in walk_contents:
                        properties[key] = walk_contents[key][:property_value_max]
                    if len(ancestors_text) > 0:
                        properties['_tags'] = ancestors_text[:property_value_max]

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
