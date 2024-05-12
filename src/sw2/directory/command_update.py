import json
import json
import sys

from sw2.directory.list import get_directories
from sw2.site.resources import update_resources

def sw2_parser_directory_update(subparser):
    parser = subparser.add_parser('update', help='update site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_directory_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_json = args.get('json')
    args_push = args.get('push')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    for directory in directories:
        for site in directory['sites']:
            resources = update_resources(site, push=args_push)
            if resources is None:
                return 1

            if args_json:
                print(json.dumps(resources))
            else:
                if args_push:
                    for r in resources:
                        print(r['uri'], ';'.join([f'{x["key"]}={x["value"]}' for x in r['properties']]))
                else:
                    for r in resources:
                        print(r['uri'], ';'.join(list(map(lambda x: f'{x}={r["properties"][x]}', r['properties'].keys()))))

    return 0