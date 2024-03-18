import json
import json
import requests
import sys
from sw2.env import Environment
from sw2.util import is_uuid

def get_sites(name, directory=None, strict=False, single=False):
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
            if directory:
                options.append('='.join(['directory', directory]))
    else:
        if directory:
            options.append('='.join(['directory', directory]))
    if strict:
        options.append('='.join(['strict', 'true']))
    query = '?'.join([Environment().apiSites() + id, '&'.join(options)])

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

    sites = json.loads(res.text)

    if single:
        if type(sites) is dict:
            return sites
        else:
            if len(sites) == 0:
                print(f'No directory found', file=sys.stderr)
                return None
            elif len(sites) > 1:
                print(f'Multiple directories found', file=sys.stderr)
                return None
            else:
                return sites[0]
    else:
        if type(sites) is dict:
            sites = [sites]
        return sites