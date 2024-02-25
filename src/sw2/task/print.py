import json
from sw2.task.site_structure import get_site_structure

def sw2_parser_task_print(subparser):
    parser = subparser.add_parser('print', help='print target site list')
    parser.add_argument('directory', nargs=1, help='directory id, name, "all" or "test:url"')
    parser.add_argument('site', nargs='?', default=None, help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_task_print(args):
    args_directory = args.get('directory')[0]
    args_site = args.get('site')
    args_all = args.get('all')
    args_strict = args.get('strict')

    structure = get_site_structure(args_directory, args_site, strict=args_strict, all=args_all)
    print(json.dumps(structure))

    return 0