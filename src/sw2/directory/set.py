import json
import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment

def set_directory_variables(id, key, value):
    headers = {}
    query = urljoin(Environment().apiDirectories(), f'{id}/metadata?key={key}&value={value}')

    res = None
    try:
        res = requests.post(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    metadata = json.loads(res.text)
    return metadata