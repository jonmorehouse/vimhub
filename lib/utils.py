import os
import config
import urllib
import urllib2
import re
import sys
import json
import github 
import time

try:
    import vim
except ImportError:
    vim = False

path_hash = {}
url_hash = {}

def td_string(minutes): 
    # convert a clever string from a time delta
    pass

def args_to_kwargs(args, kwargs):

    for arg in args:
        # get the uri 
        if "/" in arg and github.has_issues(arg):
            kwargs["repo"] = arg
        elif not "=" in arg and github.user_repo(arg):
            kwargs["repo"] = github.user_repo(arg)
        # state arguments
        elif "=" in arg: 
            # break up the pieces and then fill kwargs
            pieces = re.findall(r"[\w'=,]+", arg)
            for piece in pieces: 
                # if no equal sign - assign to state
                if not "=" in piece:
                    if piece in ("open", "closed", "state"):
                        kwargs["state"] = piece
                    continue
                # user passed in custom params for github query
                p = tuple(re.split(r"[=]+", piece))
                kwargs[p[0]] = p[1]
        else: # pass standard string arguments back to the caller
            if not kwargs.get("args"):
                kwargs["args"] = []
            kwargs["args"].append(arg)

    # no repo - try to grab from the path
    if not kwargs.get("repo"):
        kwargs["repo"] = github.repo_from_path()

    return kwargs

def equal_dicts(d1, d2):

    if json.dumps(d1) == json.dumps(d2):
        return True
    return False

def trim_lines(li):

    li = "\n".join(li)
    for i in range(li.count("\n")):
        li = li.strip()
    return li

def get_buffer(buffer_name, delete = False): 

    # only create a new window if required
    if not config.same_window:
        vim.command("silent new")

    # open buffer ...
    vim.command("edit %s" % buffer_name)
    # clear the buffer
    vim.command("1,$d")
    # set it as no file - we're not directly saving any of these buffers to disk
    vim.command("set buftype=nofile")
    return vim.current.buffer


def log(msg, error = False):

    vim.command("echom \"%s\"" % msg)

# removes any null/empty elements as well as any specified keys
def clean_data(data, banned_keys = (), rename_keys = ()):

    for key in data.keys():
        value = data.get(key)
        if not value or value and key in banned_keys:
            del data[key]
        if type(value) == str and value.lower() == "none" or value == " ":
            del data[key]
        # keep lists by default
        if type(value) == list:
            data[key] = filter(lambda a: a not in (None, "", False, " "), value)

    # rename keys as requested
    for rename in rename_keys:
        val = data.get(rename[0])
        if val:
            data[rename[1]] = val
            del data[rename[0]]

    return data

