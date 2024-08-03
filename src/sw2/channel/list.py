import json
import json
import re
import requests
import sys

from sw2.env import Environment
from sw2.util import is_uuid

def get_channel(id):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiChannels() + id

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    channel = json.loads(res.text)
    return channel

def list_channels(name, strict=False):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiChannels()

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    channel_id_names = json.loads(res.text)

    if name is None or name.lower() == 'all':
        return channel_id_names
    else:
        target_id_names = []
        for channel_id_name in channel_id_names:
            if strict:
                if name == channel_id_name['name']:
                    target_id_names.append(channel_id_name)
            else:
                if re.search(name, channel_id_name['name']):
                    target_id_names.append(channel_id_name)
        return target_id_names

def get_channels(name, strict=False):
    channels = []
    if name and is_uuid(name):
        channel = get_channel(name)
        if channel is None:
            return None
        else:
            channels.append(channel)
    else:
        channels = []
        channel_id_names = list_channels(name, strict=strict)
        if channel_id_names is None:
            return None
        for id_name in channel_id_names:
            channel = get_channel(id_name['id'])
            if channel is None:
                return None
            else:
                channels.append(channel)

    return channels

def get_timestamp(channel, timestamp_text):
    if timestamp_text is None:
        print(f'No timestamp text', file=sys.stderr)
        return None
    elif timestamp_text == 'latest':
        latest = None
        for timestamp in channel['timestamps']:
            if latest is None or timestamp > latest:
                latest = timestamp
        return latest
    else:
        pattern = timestamp_text
        matched = None
        for timestamp in channel['timestamps']:
            if timestamp.startswith(pattern):
                if matched is not None:
                    print(f'Ambiguous timestamps', file=sys.stderr)
                    return None
                matched = timestamp
        if matched is None:
            print(f'No timestamps matched', file=sys.stderr)
            return None
        return matched

def get_device_timestamp(channel, device_name, timestamp_text):
    if timestamp_text is None:
        print(f'No timestamp text', file=sys.stderr)
        return None
    elif timestamp_text == 'latest':
        latest = None
        for timestamp in channel['devices'][device_name]['timestamps']:
            if latest is None or timestamp > latest:
                latest = timestamp
        return latest
    else:
        pattern = timestamp_text
        matched = None
        for timestamp in channel['devices'][device_name]['timestamps']:
            if timestamp.startswith(pattern):
                if matched is not None:
                    print(f'Ambiguous timestamps', file=sys.stderr)
                    return None
                matched = timestamp
        if matched is None:
            print(f'No timestamps matched', file=sys.stderr)
            return None
        return matched