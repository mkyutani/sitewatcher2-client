import argparse
import io
import sys

from sw2.env import Environment
from sw2.site.add import sw2_add, sw2_parser_add
from sw2.site.collect import sw2_collect, sw2_parser_collect
from sw2.site.delete import sw2_delete, sw2_parser_delete
from sw2.site.disable import sw2_disable, sw2_parser_disable
from sw2.site.enable import sw2_enable, sw2_parser_enable
from sw2.site.list import sw2_list, sw2_parser_list
from sw2.site.rename import sw2_parser_rename, sw2_rename
from sw2.site.resources import sw2_parser_resources, sw2_resources

function_map = {
    "site": {
        "list": { "function": sw2_list, "parser": sw2_parser_list },
        "add": { "function": sw2_add, "parser": sw2_parser_add },
        "delete": { "function": sw2_delete, "parser": sw2_parser_delete },
        "rename": { "function": sw2_rename, "parser": sw2_parser_rename },
        "enable": { "function": sw2_enable, "parser": sw2_parser_enable },
        "disable": { "function": sw2_disable, "parser": sw2_parser_disable },
        "collect": { "function": sw2_collect, "parser": sw2_parser_collect },
        "resources": { "function": sw2_resources, "parser": sw2_parser_resources }
    },
    "channel": {
    }
}

def set_io_buffers():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

def main():
    set_io_buffers()

    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sp = parser.add_subparsers(dest='category', title='categories', required=True)
    for category in function_map.keys():
        ssp = sp.add_parser(category).add_subparsers(dest='method', title='methods', required=True)
        for method in function_map[category].values():
            method["parser"](ssp)

    env = Environment()
    args = parser.parse_args()
    function = function_map[args.category][args.method]["function"]

    return function(args, env)