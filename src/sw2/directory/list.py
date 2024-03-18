import json
import json
import requests
import sys

from sw2.env import Environment
from sw2.util import is_uuid

def get_directories(name, strict=False, single=False):
    if name and name.lower() == 'all':
        name = None

    headers = { 'Cache-Control': 'no-cache' }
    id = ''
    options = []
    if name:
        if is_uuid(name):
            id = name
        else:
            options.append('='.join(['name', name]))
    if strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([Environment().apiDirectories() + id, '&'.join(options)])

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

    directories = json.loads(res.text)

    if single:
        if len(directories) == 0:
            print(f'No directory found', file=sys.stderr)
            return None
        elif len(directories) > 1:
            print(f'Multiple directories found', file=sys.stderr)
            return None
        else:
            return directories[0]
    else:
        if type(directories) is dict:
            directories = [directories]
        return directories