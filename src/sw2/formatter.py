import string

class PrivateFormatter:
    class Formatter(string.Formatter):
        def get_value(self, key, *args, **kwargs):
            if key in args[1]:
                return super().get_value(key, *args, **kwargs)
            elif '_default' in args[1]:
                return args[1]['_default']
            else:
                return ''

    def __init__(self):
        pass
    def set(self, k, v):
        setattr(self, k, v)
    def get(self, k):
        return getattr(self, k)
    def format(self, t):
        f = self.Formatter()
        return f.format(t, **self.__dict__).strip()