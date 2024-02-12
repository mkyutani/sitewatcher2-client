from sw2.directory.list import list_directories
from sw2.site.list import list_sites

def get_directories(name, strict=False, all=False):
    return list_directories(name, strict, all)

def get_sites(name, strict=False):
    return list_sites(name, strict)