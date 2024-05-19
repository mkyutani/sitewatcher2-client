import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channel, get_channels

def sw2_parser_channel_delete_directory(subparser):
    aliases = ['dd']
    parser = subparser.add_parser('delete-directory', aliases=aliases, help='delete channel directory')
    parser.add_argument('channel', help='channel')
    parser.add_argument('directory', help='channel')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def sw2_channel_delete_directory(args):
    args_channel = args.get('channel')
    args_directory = args.get('directory')
    args_strict_channel = args.get('strict_channel')
    args_strict_directory = args.get('strict_directory')

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

    directory = None
    for cd in channel['directories']:
        if (args_directory == cd['id']) or (args_strict_directory and args_directory == cd['name']) or (not args_strict_directory and re.search(args_directory, cd['name'])):
            directory = cd
            break
    else:
        print('directory not found', file=sys.stderr)
        return 1

    headers = { 'Content-Type': 'application/json' }

    res = None
    try:
        res = requests.delete(urljoin(Environment().apiChannels(), '/'.join([channel['id'], 'directories', directory['id']])), headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return 1

    channel_directory_pair = json.loads(res.text)
    print(str(channel_directory_pair['channel']), str(channel_directory_pair['directory']))

    return 0
