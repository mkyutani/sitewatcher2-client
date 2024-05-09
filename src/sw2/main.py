import argparse
import io
import sys
from sw2.channel import channel_function_map
from sw2.directory import directory_function_map
from sw2.site import site_function_map

function_map = {
    'channel': { 'map': channel_function_map, 'help': 'channel' },
    'directory': { 'map': directory_function_map, 'help': 'directory' },
    'site': { 'map': site_function_map, 'help': 'site' }
}

function_aliases = {
    'channel': 'c',
    'directory': 'd',
    'site': 's'
}

def set_io_buffers():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

def main():
    set_io_buffers()

    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sp = parser.add_subparsers(dest='category', title='categories', required=True)
    for category in function_map.keys():
        ssp = sp.add_parser(category, aliases=function_aliases[category], help=function_map[category]['help']).add_subparsers(dest='method', title='methods', required=True)
        for method in function_map[category]['map'].values():
            if method['parser']:
                method['parser'](ssp)

    args = parser.parse_args()

    category = args.category
    try:
        map = function_map[category]['map']
    except KeyError:
        for key in function_aliases.keys():
            if function_aliases[key] == category:
                map = function_map[key]['map']
                break

    function = map[args.method]['function']

    return function(vars(args))