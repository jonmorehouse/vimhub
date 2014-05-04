import os

path_hash = {}

def git_path(path):

    if not path_hash.has_key(path):
        command = "cd %s && git rev-parse --show-toplevel" % path
        path_hash[path] = os.popen(command).read().strip()
    return path_hash[path]
        
def github_build_url(endpoint, token = False, params = False): 

    pass



