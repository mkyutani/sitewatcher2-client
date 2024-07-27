import json
import re
import requests
import sys
from urllib.parse import urljoin

from sw2.channel.device import output_to_device
from sw2.channel.list import get_channels
from sw2.env import Environment

def sw2_parser_channel_resources(subparser):
    parser = subparser.add_parser('resources', help='get resources of channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('--compact', action='store_true', help='in compact format')
    parser.add_argument('--device', nargs=1, default=[None], help='device name')
    parser.add_argument('--delimiter', nargs=1, default=[' '], help='delimiter')
    parser.add_argument('--json', action='store_true', help='in json format')
    parser.add_argument('--send', action='store_true', help='send to device')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    parser.add_argument('--timestamp', nargs=1, default=[None], help='timestamp or "latest"')
    return []

def get_timestamp(channel, args_timestamp):
    if args_timestamp is None:
        return None
    elif args_timestamp == 'latest':
        latest = None
        for timestamp in channel['timestamps']:
            if latest is None or timestamp['timestamp'] > latest:
                latest = timestamp['timestamp']
        return latest
    else:
        pattern = args_timestamp
        matched = None
        for timestamp in channel['timestamps']:
            if timestamp['timestamp'].startswith(pattern):
                if matched is not None:
                    print(f'Multiple timestamps matched', file=sys.stderr)
                    return None
                matched = timestamp['timestamp']
        if matched is None:
            print(f'No timestamps matched', file=sys.stderr)
            return None
        return matched

def sw2_channel_resources(args):
    args_name = args.get('name')
    args_device = args.get('device')[0]
    args_strict = args.get('strict')
    args_compact = args.get('compact')
    args_json = args.get('json')
    args_delimiter = args.get('delimiter')[0]
    args_send = args.get('send')
    args_timestamp = args.get('timestamp')[0]

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    options = []

    for channel in channels:
        print(f'Channel: {channel["id"]} {channel["name"]}')

        device_info = None
        if args_device:
            for device in channel['devices']:
                if device['name'] == args_device:
                    device_info = device
                    break
            else:
                print(f'device not found: {args_device}', file=sys.stderr)
                return 1

        headers = {}

        if device_info is None:
            query = urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'resources']))
        else:
            query = urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'resources', device_info['name']]))
            if args_send:
                options.append('log=true')

        if args_timestamp:
            timestamp = get_timestamp(channel, args_timestamp)
            if timestamp is None:
                return 1
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

        if device_info:
            channel_resources = json.loads(res.text)
            output_to_device(device_info, channel_resources, sending=args_send)
        elif args_json:
            print(res.text)
        else:
            channel_resources = json.loads(res.text)
            if args_compact:
                name = None
                for channel_resource in channel_resources:
                    for kv in channel_resource['kv']:
                        if kv['key'] == 'name':
                            name = kv['value']
                            break
                    print(channel_resource['timestamp'], channel_resource['channel_name'], channel_resource['site_name'], name, sep=args_delimiter)
            else:
                for channel_resource in channel_resources:
                    print(channel_resource['channel'])
                    for kv in channel_resource['kv']:
                        print(f'- {kv["key"]}:{kv["value"]}')

    return 0