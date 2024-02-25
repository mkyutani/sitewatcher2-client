from sw2.site.func_add import sw2_site_add, sw2_parser_site_add
from sw2.site.func_delete import sw2_site_delete, sw2_parser_site_delete
from sw2.site.func_directory import sw2_parser_site_directory, sw2_site_directory
from sw2.site.func_disable import sw2_site_disable, sw2_parser_site_disable
from sw2.site.func_enable import sw2_site_enable, sw2_parser_site_enable
from sw2.site.func_list import sw2_site_list, sw2_parser_site_list
from sw2.site.func_rename import sw2_parser_site_rename, sw2_site_rename
from sw2.site.func_resources import sw2_parser_site_resources, sw2_site_resources
from sw2.site.func_set import sw2_parser_site_set, sw2_site_set
from sw2.site.func_unset import sw2_parser_site_unset, sw2_site_unset
from sw2.site.func_variables import sw2_parser_site_variables, sw2_site_variables

site_function_map = {
    'add': { 'function': sw2_site_add, 'parser': sw2_parser_site_add },
    'delete': { 'function': sw2_site_delete, 'parser': sw2_parser_site_delete },
    'directory': { 'function': sw2_site_directory, 'parser': sw2_parser_site_directory },
    'disable': { 'function': sw2_site_disable, 'parser': sw2_parser_site_disable },
    'enable': { 'function': sw2_site_enable, 'parser': sw2_parser_site_enable },
    'list': { 'function': sw2_site_list, 'parser': sw2_parser_site_list },
    'rename': { 'function': sw2_site_rename, 'parser': sw2_parser_site_rename },
    'resources': { 'function': sw2_site_resources, 'parser': sw2_parser_site_resources },
    'set': { 'function': sw2_site_set, 'parser': sw2_parser_site_set },
    'unset': { 'function': sw2_site_unset, 'parser': sw2_parser_site_unset },
    'variables': { 'function': sw2_site_variables, 'parser': sw2_parser_site_variables }
}