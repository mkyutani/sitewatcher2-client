import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channels
from sw2.site.list import get_sites

def sw2_parser_channel_add_site(subparser):
    aliases = ['as']
    parser = subparser.add_parser('add-site', aliases=aliases, help='add channel site')
    parser.add_argument('channel', help='channel')
    parser.add_argument('site', help='channel')
    parser.add_argument('title', help='title template')
    parser.add_argument('description', help='description template')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-site', action='store_true', help='site name strict mode')
    return aliases

def sw2_channel_add_site(args):
    args_channel = args.get('channel')
    args_site = args.get('site')
    args_title = args.get('title')
    args_description = args.get('description')
    args_strict_channel = args.get('strict-channel')
    args_strict_site = args.get('strict-site')

    if is_uuid(args_channel):
        channel_id = args_channel
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

        channel_id = channels[0]['id']

    if is_uuid(args_site):
        site_id = args_site
    else:
        sites = get_sites(args_site, strict=args_strict_site)
        if sites is None:
            return 1
        elif len(sites) == 0:
            print('site not found', file=sys.stderr)
            return 1
        elif len(sites) > 1:
            print('only one site allowed', file=sys.stderr)
            return 1

        site_id = sites[0]['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'title': args_title,
        'description': args_description,
    }

    res = None
    try:
        res = requests.post(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'sites', site_id])), json=contents, headers=headers)
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