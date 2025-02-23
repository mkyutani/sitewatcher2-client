import json
import sys
import requests
import yaml
from sw2.env import Environment

def sw2_parser_resource(subparser):
    parser = subparser.add_parser('resource', help='retrive a resource')
    parser.add_argument('id', help='resource id')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return []

def sw2_resource(args):
    args_id = args.get('id')
    args_json = args.get('json')
    args_yaml = args.get('yaml')

    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiResources() + args_id

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

    resource = json.loads(res.text)
    if args_json:
        json.dump(resource, sys.stdout)
    elif args_yaml:
        yaml.dump(resource, sys.stdout)
    else:
        print(f'resource {resource["resource"]}', file=sys.stderr)
        for kv in resource['kv']:
            print(f'- property {kv["key"]} {kv["value"]}')

    return 0