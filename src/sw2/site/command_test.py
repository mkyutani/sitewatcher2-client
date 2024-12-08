import json
import pprint
import sys
import yaml

from sw2.site.list import get_sites
from sw2.site.resources import test_resources
from sw2.util import analyze_rule

def sw2_parser_site_test(subparser):
    aliases = []
    parser = subparser.add_parser('test', aliases=aliases, help='test site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--unset', nargs=2, action='append', metavar=('CATEGORY', 'WEIGHT'), help='unset a rule temporarily')
    parser.add_argument('--set', nargs=3, action='append', metavar=('CATEGORY', 'WEIGHT', 'RULE'), help='set a rule temporarily')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def patch_rules(site, temporary_rules, suppressed_rules):
    for temporary_rule in temporary_rules:
        category = temporary_rule['category']
        weight = temporary_rule['weight']
        expression = temporary_rule['expression']
        new_rule = analyze_rule(category, expression)
        if new_rule is None:
            print(f'invalid rule {expression}', file=sys.stderr)
        else:
            new_rule.update({
                'weight': weight,
            })

            if category in site['rule_category_names']:
                for site_rule in site[category]:
                    if site_rule['weight'] == weight:
                        site_rule['op'] = new_rule['op']
                        site_rule['value'] = new_rule['value']
                        site_rule['dst'] = new_rule['dst']
                        site_rule['src'] = new_rule['src']
                        print(f'{category} {weight} updated', file=sys.stderr)
                        break
                else:
                    site[category].append(new_rule)
                    print(f'{category} {weight} added', file=sys.stderr)
            else:
                    site[category] = [new_rule]
                    site['rule_category_names'].append(category)
                    print(f'{category} {weight} added', file=sys.stderr)
    for suppressed_rule in suppressed_rules:
        category = suppressed_rule['category']
        weight = suppressed_rule['weight']
        if category in site['rule_category_names']:
            unset_rule_index = -1
            for i, rule in enumerate(site[category]):
                if rule['weight'] == weight:
                    unset_rule_index = i
                    break

            if unset_rule_index >= 0:
                del site[category][unset_rule_index]
                print(f'{category} {weight} removed', file=sys.stderr)
    return site

def sw2_site_test(args):
    args_name = args.get('name')
    args_unset = args.get('unset')
    args_set = args.get('set')
    args_strict = args.get('strict')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    temporary_rules = []
    if args_set is not None:
        for set_rule in args_set:
            temporary_rules.append({
                'category': set_rule[0],
                'weight': int(set_rule[1]),
                'expression': set_rule[2]
            })

    suppressed_rules = []
    if args_unset is not None:
        for unset_rule in args_unset:
            suppressed_rules.append({
                'category': unset_rule[0],
                'weight': int(unset_rule[1])
            })

    for site in sites:
        print(f'site {site["id"]} {site["name"]}')

        site = patch_rules(site, temporary_rules, suppressed_rules)

        resources = test_resources(site, all=True)
        if resources is None:
            return 1

        for resource in resources:
            print(f'resource test {resource["name"]}')
            print(f'- uri {resource["uri"]}')
            properties = resource['properties']
            for key in properties.keys():
                print(f'- property {key} {properties[key]}')

    return 0