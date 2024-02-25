from sw2.directory.list import get_directories
from sw2.directory.variables import get_directory_variables
from sw2.site.list import get_sites
from sw2.site.variables import get_site_variables

def get_site_structure(directory_name, site_name, strict=False, all=False):
    sites = []
    if directory_name is None:
        sites = get_sites(site_name, strict=strict, all=all, metadata=True)
        for s in sites:
            s['metadata']  = get_site_variables(s['id'])
            s['directory'] = get_directories(s['directory'], strict=strict, all=all, metadata=True)
            s['directory']['metadata']  = get_directory_variables(s['directory']['id'])
    else:
        directories = get_directories(directory_name, strict=strict, all=all, metadata=True)
        for directory in directories:
            directory.update({
                'metadata': get_directory_variables(directory['id'])
            })
            sites =  get_sites(site_name, directory=directory['id'], strict=strict, all=all, metadata=True)
            for site in sites:
                site.update({
                    'metadata': get_site_variables(site['id']),
                    'directory': directory
                })
    return sites