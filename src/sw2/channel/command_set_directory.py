import json
import re
import sys
from urllib.parse import urljoin
import requests

from sw2.env import Environment
from sw2.util import is_uuid
from sw2.channel.list import get_channel, get_channels

def sw2_parser_channel_set_directory_title(subparser):
    aliases = ['sdt']
    parser = subparser.add_parser('set-directory-title', aliases=aliases, help='set channel directory title')
    parser.add_argument('channel', help='channel')
    parser.add_argument('directory', help='channel')
    parser.add_argument('title', nargs='?', default='title', help='title')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def sw2_parser_channel_set_directory_description(subparser):
    aliases = ['sdd']
    parser = subparser.add_parser('set-directory-description', aliases=aliases, help='set channel directory description')
    parser.add_argument('channel', help='channel')
    parser.add_argument('directory', help='channel')
    parser.add_argument('description', nargs='?', default='name', help='description')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def sw2_parser_channel_set_directory_priority(subparser):
    aliases = ['sdp']
    parser = subparser.add_parser('set-directory-priority', aliases=aliases, help='set channel directory priority')
    parser.add_argument('channel', help='channel')
    parser.add_argument('directory', help='channel')
    parser.add_argument('priority', nargs='?', default='name', help='priority')
    parser.add_argument('--strict-channel', action='store_true', help='channel name strict mode')
    parser.add_argument('--strict-directory', action='store_true', help='directory name strict mode')
    return aliases

def get_channel_directory(channel_str, directory_str, strict_channel, strict_directory):
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

    directory = None
    for cd in channel['directories']:
        if (directory_str == cd['id']) or (strict_directory and directory_str == cd['name']) or (not strict_directory and re.search(directory_str, cd['name'])):
            directory = cd
            break
    else:
        print('directory not found', file=sys.stderr)
        return None, None

    channel_id = channel['id']
    directory_id = directory['id']

    return channel_id, directory_id

def put_channel_directory(channel_id, directory_id, contents):
    headers = { 'Content-Type': 'application/json' }
    res = None
    try:
        res = requests.put(urljoin(Environment().apiChannels(), '/'.join([channel_id, 'directories', directory_id])), json=contents, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    channel_directory = json.loads(res.text)
    return channel_directory

def sw2_channel_set_directory_title(args):
    args_channel = args.get('channel')
    args_directory = args.get('directory')
    args_title = args.get('title')
    args_strict_channel = args.get('strict-channel')
    args_strict_directory = args.get('strict-directory')

    channel_id, directory_id = get_channel_directory(args_channel, args_directory, args_strict_channel, args_strict_directory)
    if channel_id is None or directory_id is None:
        return 1

    contents = {
        'title': args_title
    }

    channel_directory = put_channel_directory(channel_id, directory_id, contents)
    if channel_directory is None:
        return 1

    print(str(channel_directory['channel']), str(channel_directory['directory']))

    return 0

def sw2_channel_set_directory_description(args):
    args_channel = args.get('channel')
    args_directory = args.get('directory')
    args_description = args.get('description')
    args_strict_channel = args.get('strict-channel')
    args_strict_directory = args.get('strict-directory')

    channel_id, directory_id = get_channel_directory(args_channel, args_directory, args_strict_channel, args_strict_directory)
    if channel_id is None or directory_id is None:
        return 1

    contents = {
        'description': args_description
    }

    channel_directory = put_channel_directory(channel_id, directory_id, contents)
    if channel_directory is None:
        return 1

    print(str(channel_directory['channel']), str(channel_directory['directory']))

    return 0

def sw2_channel_set_directory_priority(args):
    args_channel = args.get('channel')
    args_directory = args.get('directory')
    args_priority = args.get('priority')
    args_strict_channel = args.get('strict-channel')
    args_strict_directory = args.get('strict-directory')

    channel_id, directory_id = get_channel_directory(args_channel, args_directory, args_strict_channel, args_strict_directory)
    if channel_id is None or directory_id is None:
        return 1

    contents = {
        'priority': args_priority
    }

    channel_directory = put_channel_directory(channel_id, directory_id, contents)
    if channel_directory is None:
        return 1

    print(str(channel_directory['channel']), str(channel_directory['directory']))

    return 0