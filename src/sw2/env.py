import os
from dotenv import load_dotenv
from urllib.parse import urljoin

class Environment:

    env = None

    @classmethod
    def get(cls, name):
        if cls.env is None:
            cls.env = {
                'dir': '.',
                'server': 'http://localhost:18085'
            }

            load_dotenv('.env')

            dir = os.environ.get('SW2_DIR')
            if dir:
                cls.env['dir'] = dir
            server = os.environ.get('SW2_SERVER')
            if server:
                cls.env['server'] = server

        if name in cls.env:
            return cls.env[name]
        else:
            return None

    def dir(self):
        return self.get('dir')

    def server(self):
        return self.get('server')

    def apiBase(self):
        return urljoin(self.get('server'), '/api/v1/')
    def apiDirectories(self):
        return urljoin(self.apiBase(),  'directories/')
    def apiDirectoryCollectors(self):
        return urljoin(self.apiBase(),  'directoryCollectors/')
    def apiSites(self):
        return urljoin(self.apiBase(),  'sites/')
    def apiChannels(self):
        return urljoin(self.apiBase(),  'channels/')
