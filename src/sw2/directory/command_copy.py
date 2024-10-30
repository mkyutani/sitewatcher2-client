import sys
from urllib.parse import urljoin

import requests
from sw2.env import Environment
from sw2.directory.list import get_directories

def sw2_parser_directory_copy(subparser):
    aliases = []
    parser = subparser.add_parser('copy', aliases=aliases, help='copy directory rules')
    parser.add_argument('name', nargs=1, metavar='NAME', default=None, help='destination directory id, name or "all"')
    parser.add_argument('source', nargs=1, metavar='SOURCE', default=None, help='source directory id or name')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_directory_copy(args):
    args_name = args.get('name')[0]
    args_source = args.get('source')[0]
    args_strict = args.get('strict')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('site not found', file=sys.stderr)
        return 1

    directories.sort(key=lambda x: x['id'])

    sources = get_directories(args_source, strict=args_strict)
    if sources is None:
        return 1
    elif len(sources) == 0:
        print('site not found', file=sys.stderr)
        return 1
    elif len(sources) > 1:
        print('multiple sites found', file=sys.stderr)
        return 1

    source = sources[0]
    directory_rule_category_names = source['rule_category_names']
    if len(directory_rule_category_names) == 0:
        print('no rules to copy', file=sys.stderr)
        return 1

    rules = []
    for directory_rule_category_name in directory_rule_category_names:
        sorted_source_rules = sorted(source[directory_rule_category_name], key=lambda x: x['weight'])
        for source_rule in sorted_source_rules:
            rule = {}
            rule['category_name'] = directory_rule_category_name
            rule['weight'] = source_rule.get('weight')
            rule['op'] = source_rule.get('op')
            rule['src'] = source_rule.get('src')
            rule['dst'] = source_rule.get('dst')
            rule['value'] = source_rule.get('value') if source_rule.get('value') is not None else ''
            rules.append(rule)

    headers = { 'Content-Type': 'application/json' }

    for directory in directories:
        for rule in rules:
            query = urljoin(Environment().apiDirectories(), '/'.join([directory['id'], 'rules', rule['category_name'], str(rule['weight'])]))
            contents = {}
            if rule.get('op'):
                contents['op'] = rule.get('op')
            if rule.get('src'):
                contents['src'] = rule.get('src')
            if rule.get('dst'):
                contents['dst'] = rule.get('dst')
            if rule.get('value'):
                contents['value'] = rule.get('value')
            else:
                contents['value'] = ''

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

            destination_rules = res.json()
            print(directory['id'], directory['name'], destination_rules['category_name'], destination_rules['weight'])

    return 0