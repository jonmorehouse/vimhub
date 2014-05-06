import os
import config
import urllib
import urllib2
import re
import sys
import json
import time

try:
    import vim
except ImportError:
    vim = False

path_hash = {}
url_hash = {}

def same_kwargs(kw1, kw2):

    pass

def time_ago(tstring):

    pass

def trim_lines(li):

    li = "\n".join(li)
    for i in range(li.count("\n")):
        li = li.strip()
    return li
        
def set_labels():

    vim.command("set filetype=markdown")
    vim.command(":highlight String ctermfg=7")

def get_buffer(buffer_name, delete = True): 

    # first check if buffer is already open
    if int(vim.eval("bufloaded(\"%s\")" % buffer_name)):
        if delete:
            vim.command("bdelete %s" % buffer_name)
        else:
            vim.command("b %s" % buffer_name)
            return vim.current.buffer

    # only create a new window if required
    if not config.same_window:
        vim.command("silent new")

    # open buffer ...
    vim.command("edit %s" % buffer_name)
    # set it as no file - we're not directly saving any of these buffers to disk
    vim.command("set buftype=nofile")
    # set up coloring - this should be a syntax file in the future
    set_labels()
    return vim.current.buffer

def clean_data(data, banned_keys = []):

    for key, value in data.iteritems():
        if not value or value == [] or value == "" :
            banned_keys.append(key)
    for key in banned_keys:
        if data.has_key(key):
            del data[key]
    
    if len(data.keys()) == 0:
        return False
    return data

