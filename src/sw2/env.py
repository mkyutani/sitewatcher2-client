import os
from urllib.parse import urljoin

class Environment:

    env = None

    @classmethod
    def get(cls, name):
        if cls.env is None:
            cls.env = {
                "directory": ".",
                "server": "http://localhost:8089"
            }

            dir = os.environ.get('SW2_DIR')
            if dir:
                cls.env["directory"] = dir
            server = os.environ.get('SW2_SERVER')
            if server:
                cls.env["server"] = server

        if name in cls.env:
            return cls.env[name]
        else:
            return None

    def dir(self):
        return self.get("dir")

    def server(self):
        return self.get("server")

    def apiBase(self):
        return urljoin(self.get("server"), "/api/v1/")
    def apiSites(self):
        return urljoin(self.apiBase(),  "sites/")
    def apiChannels(self):
        return urljoin(self.apiBase(),  "channels/")
