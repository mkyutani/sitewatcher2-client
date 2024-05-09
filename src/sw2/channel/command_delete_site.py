import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channel, get_channels

def sw2_parser_channel_delete_site(subparser):
    parser = subparser.add_parser('delete-site', help='delete channel site')
    parser.add_argument('channel', help='channel')
    parser.add_argument('site', help='channel')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-site', action='store_true', help='site name strict mode')

def sw2_channel_delete_site(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
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

    headers = { 'Content-Type': 'application/json' }

    res = None
    try:
        res = requests.delete(urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'sites', site['id']])), headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel_site_pair = json.loads(res.text)
    print(str(channel_site_pair['channel']), str(channel_site_pair['site']))

    return 0
