import argparse
import io
import sys
from sw2.add import sw2_add, sw2_parser_add
from sw2.collect import sw2_collect, sw2_parser_collect
from sw2.delete import sw2_delete, sw2_parser_delete
from sw2.disable import sw2_disable, sw2_parser_disable
from sw2.enable import sw2_enable, sw2_parser_enable
from sw2.env import Environment
from sw2.list import sw2_list, sw2_parser_list
from sw2.rename import sw2_parser_rename, sw2_rename
from sw2.resources import sw2_parser_resources, sw2_resources

functions = {
    "list": { "function": sw2_list, "parser": sw2_parser_list },
    "add": { "function": sw2_add, "parser": sw2_parser_add },
    "delete": { "function": sw2_delete, "parser": sw2_parser_delete },
    "rename": { "function": sw2_rename, "parser": sw2_parser_rename },
    "enable": { "function": sw2_enable, "parser": sw2_parser_enable },
    "disable": { "function": sw2_disable, "parser": sw2_parser_disable },
    "collect": { "function": sw2_collect, "parser": sw2_parser_collect },
    "resources": { "function": sw2_resources, "parser": sw2_parser_resources }
}

def set_io_buffers():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

def main():
    set_io_buffers()

    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sp = parser.add_subparsers(dest='function', title='functions')
    for function in functions.values():
        function["parser"](sp)

    if len(sys.argv) == 1:
        print(parser.format_usage(), file=sys.stderr)
        return 1

    env = Environment()
    args = parser.parse_args()
    function = functions[args.function]["function"]

    return function(args, env)