import json
import sys

from sw2.site.list import get_sites
from sw2.site.update import update_site_resources

def sw2_parser_site_update(subparser):
    parser = subparser.add_parser('update', help='update site resources')
    parser.add_argument('name', help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--initial', action='store_true', help='initial update')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_site_update(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_all = args.get('all')
    args_initial = args.get('initial')
    args_json = args.get('json')
    args_push = args.get('push')

    sites = get_sites(args_name, strict=args_strict)
    if sites is None:
        return 1
    elif len(sites) == 0:
        print('site not found', file=sys.stderr)
        return 1

    all_messages = []
    for site in sites:
        messages = update_site_resources(site, push=args_push, initial=args_initial)
        for message in messages:
            if args_all or message['op'] in '+-':
                if args_json:
                    all_messages.append(message)
                else:
                    print(message['op'], message['message'])

    if args_json:
        print(json.dumps(all_messages))

    return 0