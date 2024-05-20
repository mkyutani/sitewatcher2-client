from sw2.site.command_add import sw2_site_add, sw2_parser_site_add
from sw2.site.command_delete import sw2_site_delete, sw2_parser_site_delete
from sw2.site.command_directory import sw2_parser_site_directory, sw2_site_directory
from sw2.site.command_list import sw2_site_list, sw2_parser_site_list
from sw2.site.command_rename import sw2_parser_site_rename, sw2_site_rename
from sw2.site.command_resources import sw2_parser_site_resources, sw2_site_resources
from sw2.site.command_rules import sw2_parser_site_rules, sw2_site_rules
from sw2.site.command_set import sw2_parser_site_set, sw2_site_set
from sw2.site.command_test import sw2_parser_site_test, sw2_site_test
from sw2.site.command_update import sw2_parser_site_update, sw2_site_update
from sw2.site.command_unset import sw2_parser_site_unset, sw2_site_unset

site_function_map = {
    'add': { 'function': sw2_site_add, 'parser': sw2_parser_site_add },
    'delete': { 'function': sw2_site_delete, 'parser': sw2_parser_site_delete },
    'directory': { 'function': sw2_site_directory, 'parser': sw2_parser_site_directory },
    'list': { 'function': sw2_site_list, 'parser': sw2_parser_site_list },
    'rename': { 'function': sw2_site_rename, 'parser': sw2_parser_site_rename },
    'resources': { 'function': sw2_site_resources, 'parser': sw2_parser_site_resources },
    'rules': { 'function': sw2_site_rules, 'parser': sw2_parser_site_rules },
    'set': { 'function': sw2_site_set, 'parser': sw2_parser_site_set },
    'test': { 'function': sw2_site_test, 'parser': sw2_parser_site_test },
    'unset': { 'function': sw2_site_unset, 'parser': sw2_parser_site_unset },
    'update': { 'function': sw2_site_update, 'parser': sw2_parser_site_update }
}