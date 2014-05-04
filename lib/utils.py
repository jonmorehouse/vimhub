import os
import config
import urllib
import urllib2
import re
import json

path_hash = {}
url_hash = {}

def error_handler(msg):

    if config.debug:
        print msg

def git_path(path):

    if not path_hash.has_key(path):
        command = "cd %s && git rev-parse --show-toplevel" % path
        path_hash[path] = os.popen(command).read().strip()
    return path_hash[path]
        
def github_url(endpoint, params = {}): 

    path = os.path.join(config.api_url, endpoint)
    if not params.has_key("access_token"):
        params["access_token"] = config.access_token
    # generate path by combining params with the base url
    path += "?%s" % urllib.urlencode(params)
    return path

def github_request(url, method = "get", data = None, limit = config.max_api_pages):

    global url_hash

    # check the hash
    if method == "get" and url_hash.has_key(url):
        return url_hash[url], True

    status = False
    try: 
        request = urllib2.Request(url)
        request.get_method = lambda: method.upper()
        res = urllib2.urlopen(request)
        res_data = json.loads(res.read()) 
        res_headers = res.info()
        status = True
    except urllib2.URLError as e:
        res = e
    except urllib2.HTTPError as e:
        res = e
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
    next_data, status = github_request(next_url, method, data, limit - 1)

    # api call failed. Return whatever was returned - assume entire api call failed
    if not status:
        return next_data, status
    # successfully return everything
    return res_data + next_data, status


