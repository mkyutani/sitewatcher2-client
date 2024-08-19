import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.site.link_list import get_list_links
from sw2.site.list import get_sites
from sw2.env import Environment

def get_resources(id):
    query = urljoin(Environment().apiSites(), f'{id}/resources')

    res = None
    try:
        res = requests.get(query)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    resources = json.loads(res.text)
    return resources

def push_resource(site, uri, properties):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': uri,
        'properties': properties
    }

    query = urljoin(Environment().apiSites(), f'{site}/resources')

    res = None
    try:
        res = requests.post(query, json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    if res.status_code == 204:
        return None
    else:
        resource = json.loads(res.text)
        return resource

def test_resource_by_rules(site, link):
    excludes = site.get('exclude')
    if excludes is not None:
        excludes.sort(key=lambda x: x.get('tag'))
        for exclude in excludes:
            condition = exclude['value']
            try:
                property_name, pattern = condition.split(':', 1)
                property_text = link['properties'].get(property_name)
                if property_text is not None and re.search(pattern, property_text):
                    return False, f'{link["name"]} ({property_name}:{property_text}) excluded by rule [{condition}]'
            except ValueError:
                return False, f'Invalid rule [{condition}]'

    includes = site.get('include')
    if includes is not None:
        includes.sort(key=lambda x: x.get('tag'))
        for include in includes:
            condition = include['value']
            try:
                property_name, pattern = condition.split(':', 1)
                property_text = link['properties'].get(property_name)
                if property_text is not None and re.search(pattern, property_text):
                    break
            except ValueError:
                return False, f'Invalid rule [{condition}]'
        else:
            return False, f'{link["name"]} not included'

    return True, None

def extend_properties(site, link):
    property_templates = site.get('property_template')
    if property_templates is not None:
        property_template_details = []
        for property_template_detail in property_templates:
            tag = property_template_detail['tag']
            value = property_template_detail['value']

            variables = tag.split(':')
            if len(variables) != 3:
                print(f'Invalid property template tag [{tag}]', file=sys.stderr)
            else:
                property_template_weight = int(variables[0])
                target_name = variables[1]
                source_name = variables[2]
            source = link['properties'].get(source_name)
            if source is None:
                print(f'Property [{source_name}] not found', file=sys.stderr)
                continue

            sep = value[0]
            operands = value[1:].split(sep)
            if len(operands) < 2 or len(operands) > 3:
                print(f'Invalid property template value [{tag}]', file=sys.stderr)
                continue
            pattern = operands[0]
            compiled_pattern = re.compile(pattern)
            if len(operands) == 2:
                op = 'match'
                repl = None
            else:
                op = 'replace'
                repl = eval('"' + operands[1] + '"') # convert raw string to string

            property_template_details.append({
                'weight': property_template_weight,
                'target_name': target_name,
                'source_name': source_name,
                'source': source,
                'op': op,
                'pattern': compiled_pattern,
                'repl': repl
            })

        property_template_details.sort(key=lambda x: x.get('weight'))

        for property_template_detail in property_template_details:
            if property_template_detail['repl'] is None:
                matched = re.search(property_template_detail['pattern'], property_template_detail['source'])
                if matched is not None:
                    link['properties'][property_template_detail['target_name']] = matched.group()
            else:
                matched = re.sub(property_template_detail['pattern'], property_template_detail['repl'], property_template_detail['source'])
                print(property_template_detail['pattern'], property_template_detail['repl'], property_template_detail['source'], matched)
                if matched is not None:
                    link['properties'][property_template_detail['target_name']] = matched

def get_unknown_links(site, links):
    resources = get_resources(site['id'])
    if resources is None:
        return links

    resource_uris = [resource['uri'] for resource in resources]
    unknown_links = [link for link in links if link['uri'] not in resource_uris]
    return unknown_links

def test_resources(site, all=False):
    all_links = get_list_links(site['uri'])
    if all:
        links = all_links
    else:
        links = get_unknown_links(site, all_links)

    resources = []
    for link in links:
        result, reason = test_resource_by_rules(site, link)
        if result:
            extend_properties(site, link)
            print(f'Posting {link["uri"]}...', file=sys.stderr)
            resources.append(link)
        else:
            print(reason, file=sys.stderr)

    return resources

def update_resources(site):
    links = get_unknown_links(site, get_list_links(site['uri']))

    resources = []
    for link in links:
        result, reason = test_resource_by_rules(site, link)
        if result:
            extend_properties(site, link)
            resource = push_resource(site['id'], link['uri'], link['properties'])
            print(f'Posted {link["uri"]}...', file=sys.stderr)
            if resource is not None:
                resources.append(resource)
        else:
            print(reason, file=sys.stderr)

    return resources