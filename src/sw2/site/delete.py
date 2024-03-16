import sys
from urllib.parse import urljoin
import requests
from sw2.env import Environment

def delete_site(id):
    headers = {}
    query = urljoin(Environment().apiSites(), id)

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return False

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return False

    return True