import json
import json
import sys

from sw2.directory.list import get_directories
from sw2.site.resources import get_resources

def sw2_parser_directory_resources(subparser):
    aliases = []
    parser = subparser.add_parser('resources', aliases=aliases, help='get site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_directory_resources(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    result = 0

    for directory in directories:
        for site in directory['sites']:
            resources = get_resources(site['id'])
            if resources is None:
                result = 1
                continue

            if args_json:
                print(json.dumps(resources))
            else:
                for r in resources:
                    print(r['uri'])
                    properties = r['properties']
                    for kv in properties:
                        print('-', kv['key'], kv['value'], sep=args_delimiter)

    return result