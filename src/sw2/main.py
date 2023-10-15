import argparse
import io
import sys

from sw2.channel.add import sw2_channel_add, sw2_parser_channel_add
from sw2.channel.delete import sw2_channel_delete, sw2_parser_channel_delete
from sw2.channel.disable import sw2_channel_disable, sw2_parser_channel_disable
from sw2.channel.enable import sw2_channel_enable, sw2_parser_channel_enable
from sw2.channel.list import sw2_channel_list, sw2_parser_channel_list
from sw2.channel.rename import sw2_channel_rename, sw2_parser_channel_rename
from sw2.directory.add import sw2_directory_add, sw2_parser_directory_add
from sw2.directory.collect import sw2_directory_collect, sw2_parser_directory_collect
from sw2.directory.delete import sw2_directory_delete, sw2_parser_directory_delete
from sw2.directory.disable import sw2_directory_disable, sw2_parser_directory_disable
from sw2.directory.enable import sw2_directory_enable, sw2_parser_directory_enable
from sw2.directory.list import sw2_directory_list, sw2_parser_directory_list
from sw2.directory.rename import sw2_directory_rename, sw2_parser_directory_rename
from sw2.directory.status import sw2_directory_status, sw2_parser_directory_status
from sw2.env import Environment
from sw2.site.add import sw2_site_add, sw2_parser_site_add
from sw2.site.collect import sw2_site_collect, sw2_parser_site_collect
from sw2.site.delete import sw2_site_delete, sw2_parser_site_delete
from sw2.site.disable import sw2_site_disable, sw2_parser_site_disable
from sw2.site.enable import sw2_site_enable, sw2_parser_site_enable
from sw2.site.list import sw2_site_list, sw2_parser_site_list
from sw2.site.rename import sw2_parser_site_rename, sw2_site_rename
from sw2.site.resources import sw2_parser_site_resources, sw2_site_resources

function_map = {
    'directory': {
        'list': { 'function': sw2_directory_list, 'parser': sw2_parser_directory_list },
        'add': { 'function': sw2_directory_add, 'parser': sw2_parser_directory_add },
        'delete': { 'function': sw2_directory_delete, 'parser': sw2_parser_directory_delete },
        'rename': { 'function': sw2_directory_rename, 'parser': sw2_parser_directory_rename },
        'enable': { 'function': sw2_directory_enable, 'parser': sw2_parser_directory_enable },
        'disable': { 'function': sw2_directory_disable, 'parser': sw2_parser_directory_disable },
        'collect': { 'function': sw2_directory_collect, 'parser': sw2_parser_directory_collect },
        'status': { 'function': sw2_directory_status, 'parser': sw2_parser_directory_status }
    },
    'site': {
        'list': { 'function': sw2_site_list, 'parser': sw2_parser_site_list },
        'add': { 'function': sw2_site_add, 'parser': sw2_parser_site_add },
        'delete': { 'function': sw2_site_delete, 'parser': sw2_parser_site_delete },
        'rename': { 'function': sw2_site_rename, 'parser': sw2_parser_site_rename },
        'enable': { 'function': sw2_site_enable, 'parser': sw2_parser_site_enable },
        'disable': { 'function': sw2_site_disable, 'parser': sw2_parser_site_disable },
        'collect': { 'function': sw2_site_collect, 'parser': sw2_parser_site_collect },
        'resources': { 'function': sw2_site_resources, 'parser': sw2_parser_site_resources }
    },
    'channel': {
        'list': { 'function': sw2_channel_list, 'parser': sw2_parser_channel_list },
        'add': { 'function': sw2_channel_add, 'parser': sw2_parser_channel_add },
        'delete': { 'function': sw2_channel_delete, 'parser': sw2_parser_channel_delete },
        'rename': { 'function': sw2_channel_rename, 'parser': sw2_parser_channel_rename },
        'enable': { 'function': sw2_channel_enable, 'parser': sw2_parser_channel_enable },
        'disable': { 'function': sw2_channel_disable, 'parser': sw2_parser_channel_disable }
    }
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

    env = Environment()
    args = parser.parse_args()
    function = function_map[args.category][args.method]['function']

    return function(args, env)