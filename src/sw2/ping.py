from sw2.directory.list import list_directories
from sw2.env import Environment

def sw2_ping():
    server = Environment().server()
    print(f'Connecting to {server} ...', flush=True)
    result = list_directories(None)
    if result is None:
        return 1
    else:
        print('ok')
        return 0