import json
import os
from urllib.parse import urljoin

class Environment:

    env = None

    config_path = os.path.expanduser('~/.sitewatcher')

    @classmethod
    def get(cls, name = None):
        if cls.env is None:
            cls.env = {
                'server': 'http://localhost:18085'
            }

            if os.path.exists(cls.config_path) and os.path.isfile(cls.config_path):
                 with open(cls.config_path, 'r') as f:
                    config = json.load(f)
                    if 'server' in config:
                        cls.env['server'] = config['server']

            server = os.environ.get('SW2_SERVER')
            if server:
                cls.env['server'] = server

        if name is None:
            return cls.env
        elif name in cls.env:
            return cls.env[name]
        else:
            return None

    @classmethod
    def set(cls, name, value):
        config = {}
        if os.path.exists(cls.config_path) and os.path.isfile(cls.config_path):
            with open(cls.config_path, 'r') as f:
                config = json.load(f)

        config[name] = value

        with open(cls.config_path, 'w') as f:
            json.dump(config, f)

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
    def apiResources(self):
        return urljoin(self.apiBase(),  'resources/')