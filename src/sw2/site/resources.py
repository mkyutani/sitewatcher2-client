import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.formatter import PrivateFormatter
from sw2.site.link_list import get_list_links
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

def put_resource(site, uri, properties):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': uri,
        'properties': properties
    }

    query = urljoin(Environment().apiSites(), f'{site}/resources')

    res = None
    try:
        res = requests.put(query, json=contents, headers=headers)
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

def delete_resource(site, uri):
    headers = { 'Content-Type': 'application/json' }
    contents = {
        'uri': uri
    }

    query = urljoin(Environment().apiSites(), f'{site}/resources')

    res = None
    try:
        res = requests.delete(query, json=contents, headers=headers)
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

def initialize_resource_started_status(site):
    starts = site.get('integrated_rules').get('start')
    if starts is None:
        started = True
    else:
        started = False
    return started

def test_resource_by_rules(site, link, started):
    if not started:
        starts = site.get('integrated_rules').get('start')
        if starts is not None:
            starts.sort(key=lambda x: x.get('weight'))
            for start in starts:
                src = start.get('src')
                pattern = start.get('value')
                if src is None or pattern is None:
                    print(f'Invalid start rule (weight={weight})', file=sys.stderr)
                    continue
                property_value = link['properties'].get(src)
                if (property_value is None and pattern.lower() == 'none') or (property_value is not None and re.search(pattern, property_value)):
                        return False, f'{link["name"]} ({src}:{property_value}) triggers to start by rule [{pattern}]', True
        return False, f'{link["name"]} not started', False

    stops = site.get('integrated_rules').get('stop')
    if stops is not None:
        stops.sort(key=lambda x: x.get('weight'))
        for stop in stops:
            src = stop.get('src')
            pattern = stop.get('value')
            if src is None or pattern is None:
                print(f'Invalid stop rule (weight={weight})', file=sys.stderr)
                continue
            property_value = link['properties'].get(src)
            if (property_value is None and pattern.lower() == 'none') or (property_value is not None and re.search(pattern, property_value)):
                    return False, f'{link["name"]} ({src}:{property_value}) triggers to stop by rule [{pattern}]', False

    excludes = site.get('integrated_rules').get('exclude')
    if excludes is not None:
        excludes.sort(key=lambda x: x.get('weight'))
        for exclude in excludes:
            weight = exclude.get('weight')
            src = exclude.get('src')
            pattern = exclude.get('value')
            if src is None or pattern is None:
                print(f'Invalid exclude rule (weight={weight})', file=sys.stderr)
                continue
            property_value = link['properties'].get(src)
            if (property_value is None and pattern.lower() == 'none') or (property_value is not None and re.search(pattern, property_value)):
                    return False, f'{link["name"]} ({src}:{property_value}) excluded by rule [{pattern}]', started

    includes = site.get('integrated_rules').get('include')
    if includes is not None:
        includes.sort(key=lambda x: x.get('weight'))
        for include in includes:
            weight = include.get('weight')
            src = include.get('src')
            pattern = include.get('value')
            if src is None or pattern is None:
                print(f'Invalid include rule (weight={weight})', file=sys.stderr)
                continue
            property_value = link['properties'].get(src)
            if (property_value is None and pattern.lower() == 'none') or (property_value is not None and re.search(pattern, property_value)):
                break
        else:
            return False, f'{link["name"]} not included', started

    return True, None, started

def extend_properties(site, link):
    link['properties']['_site'] = site['id']
    link['properties']['_site_name'] = site['name']
    link['properties']['_site_uri'] = site['uri']
    link['properties']['_directory'] = site['directory']['id']
    link['properties']['_directory_name'] = site['directory']['name']

    property_templates = site.get('integrated_rules').get('property')
    if property_templates is not None:
        property_templates.sort(key=lambda x: x.get('weight'))

        for property_template in property_templates:
            weight = property_template.get('weight')
            op = property_template.get('op')
            src = property_template.get('src')
            dst = property_template.get('dst')
            value = property_template.get('value')
            if value is None:
                value = ''

            if op is None:
                print(f'Operation is not defined in property template (weight={weight})', file=sys.stderr)
                continue

            op = op.lower()

            if op == 'set':
                if dst is None:
                    print(f'Destination property name is necessary for set operation (weight={weight})', file=sys.stderr)
                    continue

                formatter = PrivateFormatter()
                for property_name in link['properties'].keys():
                    formatter.set(property_name, link['properties'][property_name])
                link['properties'][dst] = formatter.format(value)
            elif op == 'match':
                if src is None or dst is None or value is None or len(value) <= 2:
                    print(f'Source, destination and template value are necessary for match operation (weight={weight})', file=sys.stderr)
                    continue

                source = link['properties'].get(src)
                if source is None:
                    print(f'Property {src} not found', file=sys.stderr)
                    continue

                sep = value[0]
                operands = value[1:].split(sep)
                if len(operands) < 2 or len(operands) > 3:
                    print(f'Invalid property template value (weight={weight})', file=sys.stderr)
                    continue

                pattern = operands[0]
                compiled_pattern = re.compile(pattern)
                if len(operands) == 2:
                    matched = re.search(compiled_pattern, source)
                    if matched is not None:
                        link['properties'][dst] = matched.group()
                else:
                    replaced = operands[1]
                    matched, count = re.subn(compiled_pattern, replaced, source)
                    if count > 0 and matched is not None:
                        link['properties'][dst] = matched
            elif op == 'none':
                pass
            else:
                print(f'Unknown operation {property_template["op"]}', file=sys.stderr)

def classify_links(site, links):
    resources = get_resources(site['id'])
    if resources is None:
        return links

    resource_uris = [resource['uri'] for resource in resources]
    unknown_links = []
    known_links = []
    for link in links:
        if link['uri'] not in resource_uris:
            unknown_links.append(link)
        else:
            known_links.append(link)

    all_links = [link['uri'] for link in links]
    missing_resources = []
    for resource in resources:
        if resource['uri'] not in all_links:
            missing_resources.append(resource)

    return unknown_links, known_links, missing_resources

def get_unknown_links(site, links):
    unknown_links, _, _ = classify_links(site, links)
    return unknown_links

def get_known_links(site, links):
    _, known_links, _ = classify_links(site, links)
    return known_links

def integrate_rules(site):
    integrated_rules = {}
    integrated_rules['rule_category_names'] = []
    integrated_rule_weights = {}

    for rule_category_name in site.get('rule_category_names'):
        for rule in site.get(rule_category_name):
            if rule_category_name not in integrated_rules['rule_category_names']:
                integrated_rules['rule_category_names'].append(rule_category_name)
                integrated_rules[rule_category_name] = []
                integrated_rule_weights[rule_category_name] = []
            integrated_rules[rule_category_name].append({
                'weight': rule.get('weight'),
                'op': rule.get('op'),
                'src': rule.get('src'),
                'dst': rule.get('dst'),
                'value': rule.get('value')
            })
            integrated_rule_weights[rule_category_name].append(rule['weight'])

    directory = site.get('directory')
    for directory_rule_category_name in directory.get('rule_category_names'):
        for rule in directory.get(directory_rule_category_name):
            if directory_rule_category_name not in integrated_rules['rule_category_names']:
                if directory_rule_category_name not in integrated_rules['rule_category_names']:
                    integrated_rules['rule_category_names'].append(directory_rule_category_name)
                    integrated_rules[directory_rule_category_name] = []
                    integrated_rule_weights[directory_rule_category_name] = []
            if rule['weight'] not in integrated_rule_weights[directory_rule_category_name]:
                integrated_rules[directory_rule_category_name].append({
                    'weight': rule.get('weight'),
                    'op': rule.get('op'),
                    'src': rule.get('src'),
                    'dst': rule.get('dst'),
                    'value': rule.get('value')
                })
                integrated_rule_weights[directory_rule_category_name].append(rule['weight'])

    for rule_category_name in integrated_rules['rule_category_names']:
        integrated_rules[rule_category_name].sort(key=lambda x: x.get('weight'))

    site.update({'integrated_rules': integrated_rules})

    return site

def test_resources(site, all=False):
    site = integrate_rules(site)

    all_links = get_list_links(site['uri'], link_list_rules=site.get('integrated_rules').get('walk'))
    if all:
        links = all_links
    else:
        links = get_unknown_links(site, all_links)

    resources = []
    started = initialize_resource_started_status(site)
    for link in links:
        result, reason, started = test_resource_by_rules(site, link, started)
        if result:
            extend_properties(site, link)
            resources.append(link)
        else:
            print(reason, file=sys.stderr)

    return resources

def update_resources(site):
    site = integrate_rules(site)

    links = get_unknown_links(site, get_list_links(site['uri'], link_list_rules=site.get('integrated_rules').get('walk')))

    resources = []
    started = initialize_resource_started_status(site)
    for link in links:
        result, reason, started = test_resource_by_rules(site, link, started)
        if result:
            extend_properties(site, link)
            resource = push_resource(site['id'], link['uri'], link['properties'])
            if resource is not None:
                resources.append(resource)
        else:
            print(reason, file=sys.stderr)

    return resources

def refresh_resources(site):
    site = integrate_rules(site)

    all_links = get_list_links(site['uri'], link_list_rules=site.get('integrated_rules').get('walk'))
    unknown_links, known_links, missing_resources = classify_links(site, all_links)

    resources = []
    started = initialize_resource_started_status(site)
    for known_link in known_links:
        result, reason, started = test_resource_by_rules(site, known_link, started)
        if result:
            extend_properties(site, known_link)
            resource = put_resource(site['id'], known_link['uri'], known_link['properties'])
            if resource is not None:
                resources.append(resource)
        else:
            print(reason, file=sys.stderr)

    resource_uris = [resource['uri'] for resource in resources]
    missing_links = [link for link in all_links if link['uri'] not in resource_uris]
    for missing_link in missing_links:
        resource = delete_resource(site['id'], missing_link['uri'])
        print(f'{missing_link["name"]} ({missing_link["uri"]}) is dismissed', file=sys.stderr)

    for missing_resource in missing_resources:
        resource = delete_resource(site['id'], missing_resource['uri'])
        print(f'{missing_resource["id"]} ({missing_resource["uri"]}) is missing', file=sys.stderr)

    return resources