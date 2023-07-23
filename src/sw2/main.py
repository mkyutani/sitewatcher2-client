import argparse
import io
import sys
from sw2.add import sw2_add, sw2_parser_add
from sw2.delete import sw2_delete, sw2_parser_delete
from sw2.env import Environment
from sw2.list import sw2_list, sw2_parser_list

functions = {
    "list": { "function": sw2_list, "parser": sw2_parser_list },
    "add": { "function": sw2_add, "parser": sw2_parser_add },
    "delete": { "function": sw2_delete, "parser": sw2_parser_delete }
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