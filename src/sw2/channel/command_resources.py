import json
import requests
import sys
from urllib.parse import urljoin

import yaml

from sw2.channel.list import get_channels, get_timestamp
from sw2.env import Environment

def sw2_parser_channel_resources(subparser):
    parser = subparser.add_parser('resources', help='get resources of channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    parser.add_argument('--timestamp', nargs=1, default=[None], help='timestamp or "latest"')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('--detail', action='store_true', help='show detail')
    format_group.add_argument('--json', action='store_true', help='in json format')
    format_group.add_argument('--yaml', action='store_true', help='in yaml format')
    return []

def sw2_channel_resources(args):
    args_name = args.get('name')
    args_strict = args.get('strict')
    args_timestamp = args.get('timestamp')[0]
    args_detail = args.get('detail')
    args_json = args.get('json')
    args_yaml = args.get('yaml')

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    all_channel_resources = []

    for channel in channels:
        print(f'channel {channel["id"]} {channel["name"]}', file=sys.stderr)

        headers = {}
        options = []

        query = urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'resources']))

        if args_timestamp:
            timestamp = get_timestamp(channel, args_timestamp)
            if timestamp is None:
                continue
            options.append(f't={timestamp}')

        if len(options) > 0:
            query = '?'.join([query, '&'.join(options)])

        res = None
        try:
            res = requests.get(query, headers=headers)
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

        if res.status_code >= 400:
            message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
            print(f'{message} ', file=sys.stderr)
            return 1

        channel_resources = json.loads(res.text)
        for channel_resource in channel_resources:
            all_channel_resources.append(channel_resource)

    if args_json:
        json.dump(all_channel_resources, sys.stdout)
    elif args_yaml:
        yaml.dump(all_channel_resources, sys.stdout)
    else:
        name = None
        for channel_resource in all_channel_resources:
            for kv in channel_resource['kv']:
                if kv['key'] == 'name':
                    name = kv['value']
                    break
            else:
                name = 'unknown'
            print(f'{channel_resource["channel_name"]} {channel_resource["timestamp"]} {channel_resource["site_name"]} {name} {channel_resource["uri"]}')
            if args_detail:
                for kv in channel_resource['kv']:
                    print(f'- property {kv["key"]} {kv["value"]}')

    return 0