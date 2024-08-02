import json
import sys
import yaml

from sw2.site.link_list import get_list_links

def sw2_parser_test(subparser):
    parser = subparser.add_parser('test', help='test links from uri')
    parser.add_argument('uri', help='url')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-d', '--detail', action='store_true', help='show detail')
    format_group.add_argument('-j', '--json', action='store_true', help='in json format')
    format_group.add_argument('-y', '--yaml', action='store_true', help='in yaml format')
    return []

def sw2_test(args):
    args_directory = args.get('uri')
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_yaml = args.get('yaml')

    links = get_list_links(args_directory)

    if args_json:
        json.dump(links, sys.stdout)
    elif args_yaml:
        yaml.dump(links, sys.stdout)
    else:
        for link in links:
            print(link['uri'], link['name'])
            if args_detail:
                for key in link['properties'].keys():
                    print(f'- {key} {link["properties"][key]}')

    return 0