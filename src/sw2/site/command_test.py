import json
from sw2.site.link_list import get_list_links

def sw2_parser_site_test(subparser):
    parser = subparser.add_parser('test', help='test links from uri')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('uri', help='url')

def sw2_site_test(args):
    args_directory = args.get('uri')
    args_json = args.get('json')

    links = get_list_links(args_directory)

    if args_json:
        print(json.dumps(links))
    else:
        for link in links:
            print(link['uri'], link['section'] if link['section'] else 'None', link['name'])

    return 0