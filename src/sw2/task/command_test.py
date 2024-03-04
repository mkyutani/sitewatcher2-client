import json
import re
from sw2.task.link_lists import get_list_links

def sw2_parser_task_test(subparser):
    parser = subparser.add_parser('test', help='test links from uri')
    parser.add_argument('uri', help='url')

def sw2_task_test(args):
    args_directory = args.get('uri')

    links = get_list_links(args_directory)
    for link in links:
        print(link['uri'], link['section'] if link['section'] else 'None', link['name'])

    return 0