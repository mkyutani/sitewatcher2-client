import json
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channels
from sw2.directory.list import get_directories

def sw2_parser_channel_add_directory(subparser):
    aliases = ['ad']
    parser = subparser.add_parser('add-directory', aliases=aliases, help='add channel directory')
    parser.add_argument('channel', help='channel')
    parser.add_argument('directory', help='channel')
    parser.add_argument('title', nargs='?', default='title', help='title template, default: "title"')
    parser.add_argument('description', nargs='?', default='name', help='description template: default: "name"')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def sw2_channel_add_directory(args):
    args_channel = args.get('channel')
    args_directory = args.get('directory')
    args_title = args.get('title')
    args_description = args.get('description')
    args_strict_channel = args.get('strict-channel')
    args_strict_directory = args.get('strict-directory')

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

    if is_uuid(args_directory):
        directory_id = args_directory
    else:
        directories = get_directories(args_directory, strict=args_strict_directory)
        if directories is None:
            return 1
        elif len(directories) == 0:
            print('directory not found', file=sys.stderr)
            return 1
        elif len(directories) > 1:
            print('only one directory allowed', file=sys.stderr)
            return 1

        directory_id = directories[0]['id']

    headers = { 'Content-Type': 'application/json' }
    contents = {
        'title': args_title,
        'description': args_description,
    }

    res = None
    try:
        res = requests.post(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'directories', directory_id])), json=contents, headers=headers)
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