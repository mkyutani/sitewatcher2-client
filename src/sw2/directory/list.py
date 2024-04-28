import json
import json
import re
import requests
import sys

from sw2.env import Environment
from sw2.util import is_uuid

def get_directory(id):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiDirectories() + id

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

    directory = json.loads(res.text)
    return directory

def list_directories(name, strict=False):
    headers = { 'Cache-Control': 'no-cache' }
    query = Environment().apiDirectories()

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

    directory_id_names = json.loads(res.text)

    if name is None or name.lower() == 'all':
        return directory_id_names
    else:
        target_id_names = []
        for directory_id_name in directory_id_names:
            if strict:
                if name == directory_id_name['name']:
                    target_id_names.append(directory_id_name)
            else:
                if re.search(name, directory_id_name['name']):
                    target_id_names.append(directory_id_name)
        return target_id_names

def get_directories(name, strict=False):
    directories = []
    if name and is_uuid(name):
        directory = get_directory(name)
        if directory is None:
            return None
        else:
            directories.append(directory)
    else:
        if name and name.islower() == 'all':
            name = None

        directories = []
        directory_id_names = list_directories(name, strict=strict)
        for id_name in directory_id_names:
            directory = get_directory(id_name['id'])
            if directory is None:
                return None
            else:
                directories.append(directory)

    return directories