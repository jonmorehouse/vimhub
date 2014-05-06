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

def error_handler(msg):

    if config.debug:
        print msg

def git_path(path = None):

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

def github_url(endpoint, params = {}): 

    if not endpoint.startswith("http"):
        path = os.path.join(config.api_url, endpoint)
        if not params.has_key("access_token"):
            params["access_token"] = config.access_token
    else: # url was passed in
        path = endpoint
    # generate path by combining params with the base url
    path += "?%s" % urllib.urlencode(params)
    return path

def github_request(url, method = "get", data = False, limit = config.max_api_pages):

    status = False
    request = urllib2.Request(url)
    if data:
       request = urllib2.Request(url, json.dumps(data))
    try: 
        request.get_method = lambda: method.upper()
        res = urllib2.urlopen(request)
        status = True
        res_data = json.loads(res.read()) 
        res_headers = res.info()
    except urllib2.URLError as e:
        res = e
    except urllib2.HTTPError as e:
        res = e
    except ValueError as e:
        return res, status
    except any as e:
        res = e
    if not status:
        return res, status

    # hash the current url - for caching!
    url_hash[url] = res_data

    # decide whether to return now or continue recursing
    if limit == 0 or not "link" in res_headers.keys(): 
        return res_data, status

    next_url_match = re.match(r"<(?P<next_url>[^>]+)>; rel=\"next\"", res_headers['Link'])
    # if there isn't another url, return current response data
    if not next_url_match:
        return res_data, status

    # get the next urls data
    next_url = next_url_match.group("next_url")
    next_data, status = github_request(next_url, method, data, int(limit) - 1)

    # api call failed. Return whatever was returned - assume entire api call failed
    if not status:
        return next_data, status
    # successfully return everything
    return res_data + next_data, status

