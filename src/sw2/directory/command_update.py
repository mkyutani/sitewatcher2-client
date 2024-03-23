import json
import json
import sys

from sw2.directory.list import get_directories
from sw2.directory.update import update_directory_resources
from sw2.site.resource import push_site_resource

def sw2_parser_directory_update(subparser):
    parser = subparser.add_parser('update', help='update site resources in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_directory_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_all = args.get('all')
    args_json = args.get('json')
    args_push = args.get('push')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    all_messages_for_json = []
    for directory in directories:
        messages = update_directory_resources(directory['id'])
        for message in messages:
            if args_push and message['op'] == '+':
                push_site_resource(message['site'], message['uri'], message['name'], "new")
            if args_all or message['op'] in '+-':
                if args_json:
                    message.update({ 'directory': directory['id'], 'directory_name': directory['name'] })
                    all_messages_for_json.append(message)
                else:
                    print(message['op'], message['message'])

    if args_json:
        print(json.dumps(all_messages_for_json))

    return 0