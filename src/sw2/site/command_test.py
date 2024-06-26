import json
from sw2.site.link_list import get_list_links

def sw2_parser_site_test(subparser):
    aliases = []
    parser = subparser.add_parser('test', aliases=aliases, help='test links from uri')
    parser.add_argument('uri', help='url')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    return aliases

def sw2_site_test(args):
    args_directory = args.get('uri')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]

    links = get_list_links(args_directory)

    if args_json:
        print(json.dumps(links))
    else:
        for link in links:
            print(link['uri'], link['name'])
            for key in link['properties'].keys():
                print('-', key, link['properties'][key], sep=args_delimiter)

    return 0