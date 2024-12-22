from sw2.directory.command_add import sw2_directory_add, sw2_parser_directory_add
from sw2.directory.command_copy import sw2_directory_copy, sw2_parser_directory_copy
from sw2.directory.command_delete import sw2_directory_delete, sw2_parser_directory_delete
from sw2.directory.command_list import sw2_directory_list, sw2_parser_directory_list
from sw2.directory.command_rename import sw2_directory_rename, sw2_parser_directory_rename
from sw2.directory.command_set import sw2_directory_set, sw2_parser_directory_set
from sw2.directory.command_unset import sw2_directory_unset, sw2_parser_directory_unset

directory_function_map = {
    'add': { 'function': sw2_directory_add, 'parser': sw2_parser_directory_add },
    'copy': { 'function': sw2_directory_copy, 'parser': sw2_parser_directory_copy },
    'delete': { 'function': sw2_directory_delete, 'parser': sw2_parser_directory_delete },
    'list': { 'function': sw2_directory_list, 'parser': sw2_parser_directory_list },
    'rename': { 'function': sw2_directory_rename, 'parser': sw2_parser_directory_rename },
    'set': { 'function': sw2_directory_set, 'parser': sw2_parser_directory_set },
    'unset': { 'function': sw2_directory_unset, 'parser': sw2_parser_directory_unset },
}