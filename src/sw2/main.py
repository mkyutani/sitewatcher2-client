import argparse
import copy
import io
import signal
import sys
from sw2.channel import channel_function_map
from sw2.config import sw2_config, sw2_parser_config
from sw2.directory import directory_function_map
from sw2.ping import sw2_parser_ping, sw2_ping
from sw2.site import site_function_map
from sw2.test import sw2_parser_test, sw2_test

function_map = {
    'channel': { 'aliases': [ 'c' ], 'map': channel_function_map, 'help': 'channel' },
    'directory': { 'aliases': [ 'd' ], 'map': directory_function_map, 'help': 'directory' },
    'site': { 'aliases': [ 's' ], 'map': site_function_map, 'help': 'site' }
}

root_function_map = {
    'ping': { 'function': sw2_ping, 'parser': sw2_parser_ping },
    'test': { 'function': sw2_test, 'parser': sw2_parser_test },
    'config': { 'function': sw2_config, 'parser': sw2_parser_config}
}

def setup():
    signal.signal(signal.SIGINT, lambda num, frame: sys.exit(1))
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=False)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=False)

def main():
    setup()

    runtime_function_map = {}
    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sp = parser.add_subparsers(dest='category', title='categories', required=True)

    for root_function in root_function_map.values():
        root_function['parser'](sp)

    for category in function_map.keys():
        runtime_function_map[category] = copy.deepcopy(function_map[category])
        category_aliases = function_map[category]['aliases']
        category_map = function_map[category]['map']
        category_help = function_map[category]['help']
        ssp = sp.add_parser(category, aliases=category_aliases, help=category_help).add_subparsers(dest='method', title='methods', required=True)
        for method in category_map.values():
            method_aliases = method['parser'](ssp)
            for method_alias in method_aliases:
                runtime_function_map[category]['map'][method_alias] = copy.deepcopy(method)
        for category_alias in category_aliases:
            runtime_function_map[category_alias] = copy.deepcopy(runtime_function_map[category])

    args = parser.parse_args()

    category = args.category
    if 'method' in dir(args):
        method = args.method
        function = runtime_function_map[category]['map'][method]['function']
        return function(vars(args))
    else:
        for root_function_name in root_function_map.keys():
            if root_function_name == category:
                return root_function_map[root_function_name]['function'](vars(args))