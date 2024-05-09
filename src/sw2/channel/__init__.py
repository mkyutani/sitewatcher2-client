from sw2.channel.command_add import sw2_channel_add, sw2_parser_channel_add
from sw2.channel.command_add_directory import sw2_channel_add_directory, sw2_parser_channel_add_directory
from sw2.channel.command_add_site import sw2_channel_add_site, sw2_parser_channel_add_site
from sw2.channel.command_delete import sw2_channel_delete, sw2_parser_channel_delete
from sw2.channel.command_delete_directory import sw2_channel_delete_directory, sw2_parser_channel_delete_directory
from sw2.channel.command_delete_site import sw2_channel_delete_site, sw2_parser_channel_delete_site
from sw2.channel.command_list import sw2_channel_list, sw2_parser_channel_list
from sw2.channel.command_rename import sw2_channel_rename, sw2_parser_channel_rename

channel_function_map = {
    'add': { 'function': sw2_channel_add, 'parser': sw2_parser_channel_add },
    'a': { 'function': sw2_channel_add, 'parser': None },
    'add-directory': { 'function': sw2_channel_add_directory, 'parser': sw2_parser_channel_add_directory },
    'ad': { 'function': sw2_channel_add_directory, 'parser': None },
    'da': { 'function': sw2_channel_add_directory, 'parser': None },
    'add-site': { 'function': sw2_channel_add_site, 'parser': sw2_parser_channel_add_site },
    'as': { 'function': sw2_channel_add_site, 'parser': None },
    'sa': { 'function': sw2_channel_add_site, 'parser': None },
    'delete': { 'function': sw2_channel_delete, 'parser': sw2_parser_channel_delete },
    'd': { 'function': sw2_channel_delete, 'parser': None },
    'delete-directory': { 'function': sw2_channel_delete_directory, 'parser': sw2_parser_channel_delete_directory },
    'dd': { 'function': sw2_channel_delete_directory, 'parser': None },
    'delete-site': { 'function': sw2_channel_delete_site, 'parser': sw2_parser_channel_delete_site },
    'ds': { 'function': sw2_channel_delete_site, 'parser': None },
    'sd': { 'function': sw2_channel_delete_site, 'parser': None },
    'list': { 'function': sw2_channel_list, 'parser': sw2_parser_channel_list },
    'l': { 'function': sw2_channel_list, 'parser': None },
    'rename': { 'function': sw2_channel_rename, 'parser': sw2_parser_channel_rename },
    'r': { 'function': sw2_channel_rename, 'parser': None }
}