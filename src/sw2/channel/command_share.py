import json
import requests
import sys
from urllib.parse import urljoin

from sw2.channel.device import output_to_device
from sw2.channel.list import get_channels, get_timestamp
from sw2.env import Environment

def sw2_parser_channel_share(subparser):
    parser = subparser.add_parser('share', help='share resources of channels')
    parser.add_argument('name', nargs='?', metavar='NAME', default=None, help='channel id, name or "all"')
    parser.add_argument('device', nargs=1, help='device name')
    parser.add_argument('--strict', action='store_true', help='strict name check')
    parser.add_argument('--timestamp', nargs=1, default=[None], help='timestamp or "latest"')
    return []

def sw2_channel_share(args):
    args_name = args.get('name')
    args_device = args.get('device')[0]
    args_strict = args.get('strict')
    args_timestamp = args.get('timestamp')[0]

    channels = get_channels(args_name, strict=args_strict)
    if channels is None:
        return 1
    elif len(channels) == 0:
        print('channel not found', file=sys.stderr)
        return 1

    options = []

    for channel in channels:
        print(f'channel {channel["id"]} {channel["name"]}', file=sys.stderr)

        headers = {}

        device_info = None
        for device in channel['devices']:
            if device['name'] == args_device:
                device_info = device
                query = urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'resources', device_info['name']]))
                break
        else:
            print(f'device not found: {args_device}', file=sys.stderr)
            continue

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
        output_to_device(device_info, channel_resources, sending=True)

    return 0