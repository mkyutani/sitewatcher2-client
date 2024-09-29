from sw2.directory.command_add import sw2_directory_add, sw2_parser_directory_add
from sw2.directory.command_delete import sw2_directory_delete, sw2_parser_directory_delete
from sw2.directory.command_list import sw2_directory_list, sw2_parser_directory_list
from sw2.directory.command_refresh import sw2_directory_refresh, sw2_parser_directory_refresh
from sw2.directory.command_resources import sw2_directory_resources, sw2_parser_directory_resources
from sw2.directory.command_rename import sw2_directory_rename, sw2_parser_directory_rename
from sw2.directory.command_set import sw2_directory_set, sw2_parser_directory_set
from sw2.directory.command_test import sw2_directory_test, sw2_parser_directory_test
from sw2.directory.command_unset import sw2_directory_unset, sw2_parser_directory_unset
from sw2.directory.command_update import sw2_directory_update, sw2_parser_directory_update

directory_function_map = {
    'add': { 'function': sw2_directory_add, 'parser': sw2_parser_directory_add },
    'delete': { 'function': sw2_directory_delete, 'parser': sw2_parser_directory_delete },
    'list': { 'function': sw2_directory_list, 'parser': sw2_parser_directory_list },
    'refresh': { 'function': sw2_directory_refresh, 'parser': sw2_parser_directory_refresh },
    'rename': { 'function': sw2_directory_rename, 'parser': sw2_parser_directory_rename },
    'resources': { 'function': sw2_directory_resources, 'parser': sw2_parser_directory_resources },
    'set': { 'function': sw2_directory_set, 'parser': sw2_parser_directory_set },
    'test': { 'function': sw2_directory_test, 'parser': sw2_parser_directory_test },
    'unset': { 'function': sw2_directory_unset, 'parser': sw2_parser_directory_unset },
    'update': { 'function': sw2_directory_update, 'parser': sw2_parser_directory_update },
}