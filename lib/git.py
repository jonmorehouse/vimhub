import os
import subprocess
import re
import utils
import config

remote_hash = {}
path_hash = {}

def remotes(path):

    if remote_hash.get(path):
        return remote_hash.get(path)

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
    
    # hash
    remote_hash[path] = remotes
    return remote_hash.get(path)

def repo_path(path = None):

    if not path:
        path = os.getcwd()

    if not path_hash.has_key(path):
        command = "cd %s && git rev-parse --show-toplevel" % path
        try:
            path_hash[path] = os.popen(command).read().strip()
        except:
            sys.exit(1)
            return
    return path_hash[path]

