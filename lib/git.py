import os
import subprocess
import re
import utils
import config

remote_hash = {}

def get_remotes(path):

    # grab only the remotes - this is safer than using python due to global character differences amongst shells (line endings etc)
    command = "cd %s && git remote -v | awk '{ print $1 \"=\" $2 }'" % path
    output = os.popen(command).read()
    remotes = {} 

    # loop through each line and generate creator/project name
    for line in output.splitlines():
        pieces = tuple(line.split("="))
        if remotes.has_key(pieces[0]):
            continue
        # split into pieces so we can abstract the relevant parts of ui
        uri_pieces = re.split(r"[\:,\/]+", pieces[1])
        # remove any trailing .gits
        project_name = re.sub(r"\.git$", "",  uri_pieces[-1])
        # grab the github username
        creator = uri_pieces[-2]
        remotes[pieces[0]] = (creator, project_name)
    return remotes
    
def get_remote(path, upstream_preferred = False):

    path = utils.git_path(path)

    # generate remote hash if not already present
    if not remote_hash.has_key(path):
        remote_hash[path] = get_remotes(path)

    # grab from the remote hash 
    def _getRemoteFromHash(remotes, preferred, unpreferred):
        k = remotes.keys()[:]
        if preferred in k:
            return remotes[preferred]
        elif len(k) == 1:
            return remotes[k[0]]
        try:
            k.remove(unpreferred)
        except:     
            pass
        return remotes[k[0]]

    # now return the correct 
    remote = _getRemoteFromHash(remote_hash[path], "origin", "upstream")
    if upstream_preferred:
        remote = _getRemoteFromHash(remote_hash[path], "upstream", "origin")
    return remote

def get_uri(path = os.getcwd(), upstream_preferred = config.upstream_issues):

    git_path = utils.git_path(path)
    remote = get_remote(git_path, upstream_preferred)
    return "/".join(remote)


