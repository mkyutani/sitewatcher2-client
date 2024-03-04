import re
import sys
from sw2.site.resource import get_site_resources
from sw2.task.link_lists import get_list_links
from sw2.task.site_resource import push_site_resource
from sw2.task.site_structure import get_site_structure

def sw2_parser_task_update(subparser):
    parser = subparser.add_parser('update', help='update site links')
    parser.add_argument('directory', nargs=1, help='directory id, name, "all"')
    parser.add_argument('site', nargs='?', default=None, help='site id, name or "all"')
    parser.add_argument('--all', action='store_true', help='print not changed links')
    parser.add_argument('--push', action='store_true', help='push to remote')
    parser.add_argument('--strict', action='store_true', help='strict name check')

def update_sites(sites, do_push=False, all=False):
    for site in sites:
        resource_dict = {}
        resources = get_site_resources(site['id'])
        if resources is not None:
            for resource in resources:
                resource_dict[resource['uri']] = resource

        messages = []

        links = get_list_links(site['uri'])
        excludes = [kv['value'] for kv in site['metadata'] if kv['key'] == 'exclude']
        unique_uris = []
        for link in links:
            message = ' '.join([link['uri'], link['name'] if link['section'] is None else f'{link["section"]}::{link["name"]}'])
            for exclude in excludes:
                if re.match(exclude, link['uri']):
                    messages.append({'message': message, 'op': 'S'})
                    break
            else:
                if link['uri'] in unique_uris:
                    messages.append({'message': message, 'op': 'D'})
                else:
                    unique_uris.append(link['uri'])
                    if resource_dict.pop(link['uri'], None) is None:
                        if do_push:
                            push_site_resource(site, link, "new")
                        messages.append({'message': message, 'op': '+'})
                    else:
                        messages.append({'message': message, 'op': ' '})
        for resource in resource_dict.values():
            message = ' '.join([resource['uri'], resource['name']])
            messages.append({'message': message, 'op': '-'})

        for message in messages:
            if all or message['op'] in '+-':
                print(message['op'], message['message'])

def sw2_task_update(args):
    args_directory = args.get('directory')[0]
    args_site = args.get('site')[0] if args.get('site') else None
    args_all = args.get('all')
    args_strict = args.get('strict')
    args_push = args.get('push')

    sites = get_site_structure(args_directory, args_site, strict=args_strict, all=args_all)
    if sites is None:
        return 1

    if len(sites) == 0:
        print(f'No such a site', file=sys.stderr)
        return 1

    update_sites(sites, do_push=args_push, all=args_all)

    return 0