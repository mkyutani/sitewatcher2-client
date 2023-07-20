import argparse
import io
import sys
from sw2.list import func_list

functions = {
    "list": func_list
}

def main():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

    parser = argparse.ArgumentParser(description='Sitewatcher2 Client Tool')
    sps = parser.add_subparsers(dest='function', title='functions')
    sps_list = sps.add_parser('list', help='list sites')
    sps_list.add_argument('name', nargs=1, metavar='NAME', help='site name')

    if len(sys.argv) == 1:
        print(parser.format_usage(), file=sys.stderr)
        return 1

    args = parser.parse_args()
    method = args.function

    functions[method](args)

    return 0