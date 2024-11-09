import json
import sys

import yaml

from sw2.channel.list import get_channels
from sw2.directory.list import get_directory
from sw2.site.list import get_site
from sw2.site.resources import refresh_resources

def sw2_parser_channel_refresh(subparser):
    parser = subparser.add_parser('refresh', help='refresh site resources in channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    return []

def refresh(site):
    resources = refresh_resources(site)
    if resources is None:
        return None

    for resource in resources:
        name = 'None'
        for kv in resource['properties']:
            if kv['key'] == '_name':
                name = kv['value']
                break
        print(f'resource {resource["id"]} {name}')
        print(f'- uri {resource["uri"]}')
        print(f'- site {resource["site"]} {resource["site_name"]}')
        print(f'- timestamp {resource["timestamp"]}')
        for kv in resource['properties']:
            print(f'- property {kv["key"]} {kv["value"]}')

    return resources

def sw2_channel_refresh(args):
    args_name = args.get('name')
    args_strict = args.get('strict')

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    channels.sort(key=lambda x: x['id'])

    for channel in channels:
        print(f'channel {channel["id"]} {channel["name"]}')
        if 'directories' in channel:
            for channel_directory in channel['directories']:
                print(f'directory {channel_directory["id"]} {channel_directory["name"]}')

                directory = get_directory(channel_directory['id'])
                if directory is None:
                    return 1

                for site in directory['sites']:
                    print(f'site {site["id"]} {site["name"]}')

                    site = get_site(site['id'])
                    if site is None:
                        return 1

                    resources = refresh_resources(site)
                    if resources is None:
                        return 1

        if 'sites' in channel:
            for channel_site in channel['sites']:
                print(f'site {channel_site["id"]} {channel_site["name"]}')

                site = get_site(channel_site['id'])
                if site is None:
                    return 1

                resources = refresh_resources(site)
                if resources is None:
                    return 1

    return 0