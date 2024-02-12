import argparse
import io
import sys
from sw2.env import Environment
from sw2.directory import directory_function_map
from sw2.site import site_function_map
from sw2.task import task_function_map

function_map = {
    'directory': directory_function_map,
    'site': site_function_map,
    'task': task_function_map
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
        ssp = sp.add_parser(category).add_subparsers(dest='method', title='methods', required=True)
        for method in function_map[category].values():
            method['parser'](ssp)

    args = parser.parse_args()
    function = function_map[args.category][args.method]['function']

    return function(vars(args))