from sw2.directory.list import list_directories
from sw2.env import Environment

def sw2_parser_ping(subparser):
    subparser.add_parser('ping', help='test connection')
    return []

def sw2_ping(args):
    server = Environment().server()
    print(f'Connecting to {server} ...', flush=True)
    result = list_directories(None)
    if result is None:
        return 1
    else:
        print('ok')
        return 0