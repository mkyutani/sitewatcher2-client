from sw2.channel.command_add import sw2_channel_add, sw2_parser_channel_add
from sw2.channel.command_add_directory import sw2_channel_add_directory, sw2_parser_channel_add_directory
from sw2.channel.command_add_site import sw2_channel_add_site, sw2_parser_channel_add_site
from sw2.channel.command_delete import sw2_channel_delete, sw2_parser_channel_delete
from sw2.channel.command_delete_directory import sw2_channel_delete_directory, sw2_parser_channel_delete_directory
from sw2.channel.command_delete_site import sw2_channel_delete_site, sw2_parser_channel_delete_site
from sw2.channel.command_list import sw2_channel_list, sw2_parser_channel_list
from sw2.channel.command_rename import sw2_channel_rename, sw2_parser_channel_rename
from sw2.channel.command_set_directory import sw2_channel_set_directory_description, sw2_channel_set_directory_title, sw2_parser_channel_set_directory_description, sw2_parser_channel_set_directory_title
from sw2.channel.command_set_site import sw2_channel_set_site_description, sw2_channel_set_site_title, sw2_parser_channel_set_site_description, sw2_parser_channel_set_site_title

channel_function_map = {
    'add': { 'function': sw2_channel_add, 'parser': sw2_parser_channel_add },
    'add-directory': { 'function': sw2_channel_add_directory, 'parser': sw2_parser_channel_add_directory },
    'add-site': { 'function': sw2_channel_add_site, 'parser': sw2_parser_channel_add_site },
    'delete': { 'function': sw2_channel_delete, 'parser': sw2_parser_channel_delete },
    'delete-directory': { 'function': sw2_channel_delete_directory, 'parser': sw2_parser_channel_delete_directory },
    'delete-site': { 'function': sw2_channel_delete_site, 'parser': sw2_parser_channel_delete_site },
    'list': { 'function': sw2_channel_list, 'parser': sw2_parser_channel_list },
    'rename': { 'function': sw2_channel_rename, 'parser': sw2_parser_channel_rename },
    'set-directory-description': { 'function': sw2_channel_set_directory_description, 'parser': sw2_parser_channel_set_directory_description },
    'set-site-description': { 'function': sw2_channel_set_site_description, 'parser': sw2_parser_channel_set_site_description },
    'set-directory-title': { 'function': sw2_channel_set_directory_title, 'parser': sw2_parser_channel_set_directory_title },
    'set-site-title': { 'function': sw2_channel_set_site_title, 'parser': sw2_parser_channel_set_site_title }
}