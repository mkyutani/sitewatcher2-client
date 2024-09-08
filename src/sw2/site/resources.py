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

def test_resource_by_rules(site, link):
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
                    return False, f'{link["name"]} ({src}:{property_value}) excluded by rule [{pattern}]'

    includes = site.get('integrated_rules').get('include')
    if includes is not None:
        includes.sort(key=lambda x: x.get('weight'))
        for include in includes:
            weight = exclude.get('weight')
            src = include.get('src')
            pattern = include.get('value')
            if src is None or pattern is None:
                print(f'Invalid include rule (weight={weight})', file=sys.stderr)
                continue
            property_value = link['properties'].get(src)
            if (property_value is None and pattern.lower() == 'none') or (property_value is not None and re.search(pattern, property_value)):
                break
        else:
            return False, f'{link["name"]} not included'

    return True, None

def extend_properties(site, link):
    property_templates = site.get('integrated_rules').get('property_template')
    if property_templates is not None:
        property_templates.sort(key=lambda x: x.get('weight'))

        for property_template in property_templates:
            weight = property_template.get('weight')
            op = property_template.get('op')
            src = property_template.get('src')
            dst = property_template.get('dst')
            value = property_template.get('value')

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
                    matched = re.sub(compiled_pattern, replaced, source)
                    if matched is not None:
                        link['properties'][dst] = matched
            elif op == 'none':
                pass
            else:
                print(f'Unknown operation {property_template["op"]}', file=sys.stderr)

def get_unknown_links(site, links):
    resources = get_resources(site['id'])
    if resources is None:
        return links

    resource_uris = [resource['uri'] for resource in resources]
    unknown_links = [link for link in links if link['uri'] not in resource_uris]
    return unknown_links

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
    site = integrate_rules(site)

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