import json
from sw2.task.list_links import get_list_links
from sw2.task.site_structure import get_site_structure

def sw2_parser_task_print(subparser):
    parser = subparser.add_parser('print', help='print target site list')
    parser.add_argument('directory', nargs=1, help='directory id, name, "all" or url')
    parser.add_argument('site', nargs='?', default=None, help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def sw2_task_print(args):
    args_directory = args.get('directory')[0]
    args_site = args.get('site')
    args_all = args.get('all')
    args_delimiter = args.get('delimiter')[0]
    args_strict = args.get('strict')

    structure = get_site_structure(args_directory, args_site, strict=args_strict, all=args_all)
    if args.get('json'):
        print(json.dumps(structure))
    else:
        for site in structure:
            print(str(site['id']), site['name'], site['directory_name'], site["uri"], 'enabled' if site['enabled'] else 'disabled', sep=args_delimiter)

    return 0