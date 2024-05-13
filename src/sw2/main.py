import argparse
import copy
import io
import sys
from sw2.channel import channel_function_map
from sw2.directory import directory_function_map
from sw2.site import site_function_map

function_map = {
    'channel': { 'aliases': [ 'c' ], 'map': channel_function_map, 'help': 'channel' },
    'directory': { 'aliases': [ 'd' ], 'map': directory_function_map, 'help': 'directory' },
    'site': { 'aliases': [ 's' ], 'map': site_function_map, 'help': 'site' }
}

def set_io_buffers():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

def main():
    set_io_buffers()

    runtime_function_map = {}
    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sp = parser.add_subparsers(dest='category', title='categories', required=True)
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
    method = args.method
    function = function_map[category]['map'][method]['function']

    return function(vars(args))