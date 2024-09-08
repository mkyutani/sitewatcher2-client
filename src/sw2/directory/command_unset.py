import requests
import sys
from urllib.parse import urljoin

from sw2.directory.list import get_directories
from sw2.env import Environment

def sw2_parser_directory_unset(subparser):
    aliases = []
    parser = subparser.add_parser('unset', aliases=aliases, help='unset rule of site in directory')
    parser.add_argument('name', help='directory id, name or "all"')
    parser.add_argument('rule', default=None, help='rule name')
    parser.add_argument('weight', default=None, help='rule weight')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return aliases

def sw2_directory_unset(args):
    args_name = args.get('name')
    args_rule = args.get('rule')
    args_weight = args.get('weight')
    args_strict = args.get('strict')

    directories = get_directories(args_name, strict=args_strict)
    if directories is None:
        return 1
    elif len(directories) == 0:
        print('directory not found', file=sys.stderr)
        return 1

    for directory in directories:
        query = urljoin(Environment().apiDirectories(), '/'.join([directory['id'], 'rules', args_rule, args_weight]))

        res = None
        try:
            res = requests.delete(query)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        print(directory['id'], directory['name'], args_rule, args_weight)

    return 0