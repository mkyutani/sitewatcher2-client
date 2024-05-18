import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channel, get_channels

def sw2_parser_channel_set_site_title(subparser):
    aliases = ['sst']
    parser = subparser.add_parser('set-site-title', aliases=aliases, help='set channel site title')
    parser.add_argument('channel', help='channel')
    parser.add_argument('site', help='channel')
    parser.add_argument('title', nargs='?', default='title', help='title')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-site', action='store_true', help='site name strict mode')
    return aliases

def sw2_parser_channel_set_site_description(subparser):
    aliases = ['ssd']
    parser = subparser.add_parser('set-site-description', aliases=aliases, help='set channel site description')
    parser.add_argument('channel', help='channel')
    parser.add_argument('site', help='channel')
    parser.add_argument('description', nargs='?', default='name', help='description')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-site', action='store_true', help='site name strict mode')
    return aliases

def sw2_channel_set_site_title(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_title = args.get('title')
    args_strict_channel = args.get('strict-channel')
    args_strict_site = args.get('strict-site')

    if is_uuid(args_channel):
        channel = get_channel(args_channel)
        if channel is None:
            return 1
    else:
        channels = get_channels(args_channel, strict=args_strict_channel)
        if channels is None:
            return 1
        elif len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return 1
        elif len(channels) > 1:
            print('only one channel allowed', file=sys.stderr)
            return 1

        channel = channels[0]

    site = None
    for cd in channel['sites']:
        if (args_site == cd['id']) or (args_strict_site and args_site == cd['name']) or (not args_strict_site and re.search(args_site, cd['name'])):
            site = cd
            break
    else:
        print('site not found', file=sys.stderr)
        return 1

    channel_id = channel['id']
    site_id = site['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'title': args_title
    }

    res = None
    try:
        res = requests.put(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'sites', site_id])), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel_site = json.loads(res.text)
    print(str(channel_site['channel']), str(channel_site['site']))

    return 0

def sw2_channel_set_site_description(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_description = args.get('description')
    args_strict_channel = args.get('strict-channel')
    args_strict_site = args.get('strict-site')

    if is_uuid(args_channel):
        channel = get_channel(args_channel)
        if channel is None:
            return 1
    else:
        channels = get_channels(args_channel, strict=args_strict_channel)
        if channels is None:
            return 1
        elif len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return 1
        elif len(channels) > 1:
            print('only one channel allowed', file=sys.stderr)
            return 1

        channel = channels[0]

    site = None
    for cd in channel['sites']:
        if (args_site == cd['id']) or (args_strict_site and args_site == cd['name']) or (not args_strict_site and re.search(args_site, cd['name'])):
            site = cd
            break
    else:
        print('site not found', file=sys.stderr)
        return 1

    channel_id = channel['id']
    site_id = site['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'description': args_description
    }

    res = None
    try:
        res = requests.put(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'sites', site_id])), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel_site = json.loads(res.text)
    print(str(channel_site['channel']), str(channel_site['site']))

    return 0