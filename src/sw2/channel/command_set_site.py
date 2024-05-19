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

def sw2_parser_channel_set_site_priority(subparser):
    aliases = ['ssp']
    parser = subparser.add_parser('set-site-priority', aliases=aliases, help='set channel site priority')
    parser.add_argument('channel', help='channel')
    parser.add_argument('site', help='channel')
    parser.add_argument('priority', nargs='?', default='name', help='priority')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-site', action='store_true', help='site name strict mode')
    return aliases

def get_channel_site(channel_str, site_str, strict_channel, strict_site):
    if is_uuid(channel_str):
        channel = get_channel(channel_str)
        if channel is None:
            return None, None
    else:
        channels = get_channels(channel_str, strict=strict_channel)
        if channels is None:
            return None, None
        elif len(channels) == 0:
            print('channel not found', file=sys.stderr)
            return None, None
        elif len(channels) > 1:
            print('only one channel allowed', file=sys.stderr)
            return None, None

        channel = channels[0]

    site = None
    for cd in channel['sites']:
        if (site_str == cd['id']) or (strict_site and site_str == cd['name']) or (not strict_site and re.search(site_str, cd['name'])):
            site = cd
            break
    else:
        print('site not found', file=sys.stderr)
        return None, None

    channel_id = channel['id']
    site_id = site['id']

    return channel_id, site_id

def put_channel_site(channel_id, site_id, contents):
    headers = { 'Content-Type': 'application/json' }
    res = None
    try:
        res = requests.put(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'sites', site_id])), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    channel_site = json.loads(res.text)
    return channel_site

def sw2_channel_set_site_title(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_title = args.get('title')
    args_strict_channel = args.get('strict_channel')
    args_strict_site = args.get('strict_site')

    channel_id, site_id = get_channel_site(args_channel, args_site, args_strict_channel, args_strict_site)
    if channel_id is None or site_id is None:
        return 1

    contents = {
        'title': args_title
    }

    channel_site = put_channel_site(channel_id, site_id, contents)
    if channel_site is None:
        return 1

    print(str(channel_site['channel']), str(channel_site['site']))

    return 0

def sw2_channel_set_site_description(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_description = args.get('description')
    args_strict_channel = args.get('strict_channel')
    args_strict_site = args.get('strict_site')

    channel_id, site_id = get_channel_site(args_channel, args_site, args_strict_channel, args_strict_site)
    if channel_id is None or site_id is None:
        return 1

    contents = {
        'description': args_description
    }

    channel_site = put_channel_site(channel_id, site_id, contents)
    if channel_site is None:
        return 1

    print(str(channel_site['channel']), str(channel_site['site']))

    return 0

def sw2_channel_set_site_priority(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_priority = args.get('priority')
    args_strict_channel = args.get('strict_channel')
    args_strict_site = args.get('strict_site')

    channel_id, site_id = get_channel_site(args_channel, args_site, args_strict_channel, args_strict_site)
    if channel_id is None or site_id is None:
        return 1

    contents = {
        'priority': args_priority
    }

    channel_site = put_channel_site(channel_id, site_id, contents)
    if channel_site is None:
        return 1

    print(str(channel_site['channel']), str(channel_site['site']))

    return 0