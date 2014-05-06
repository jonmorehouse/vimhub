import utils
import config
import os
import urllib
import urllib2
import json
import git
import re
from datetime import datetime as dt
from datetime import timedelta as td

_user = {}
_repos = {}
_offset = None

# returns a time object from a github time string
def time(ts):

    global _offset
    if not _offset:
        _offset = dt.now() - dt.utcnow()
    # get current time (UTC)
    t = dt.strptime(ts.replace("Z",""), "%Y-%m-%dT%H:%M:%S")
    return t + _offset

def user_repo(arg):

    r = "%s/%s" % (user().get("login"), arg)
    if not has_issues(r):
        return False
    return r

def user():

    global _user
    if len(_user.keys()) > 0:
        return _user

    # get data
    data, status = request(url("user"))
    # cache this hash
    _user.update(data)
    return _user

def has_issues(repo_uri):
    r = repo(repo_uri)
    if not type(r) == dict:
        return False
    return r.get("has_issues")

# prefers your username's issues over the upstream fork!
# if you have upstream and downstream then you can just pass in the uri to the parent!
def repo_from_path(path = None):

    if not path:
        path = git.repo_path()
    
    # generate all options
    uris = []
    logins = []
    for name, remote in git.remotes(path).iteritems():
        uri = "/".join(remote)
        if not has_issues(uri):
            continue
        uris.append(uri)
        logins.append(remote[0])

    # now analyze those options
    if len(uris) == 0:
        return None
    if len(uris) == 1:     
        return uris[0]
    # prefer the user over all else
    if user().get("login") in logins:
        return uris[logins.index(user().get("login"))]
    # just return the last option 
    return uris[-1]

def repo(uri):

    if _repos.get(uri):
        return _repos.get(uri)

    data, status = request(url("repos/%s" % uri))
    _repos[uri] = data
    return _repos.get(uri)
     
def url(endpoint, params = {}): 

    if not endpoint.startswith("http"):
        path = os.path.join(config.api_url, endpoint)
        if not params.has_key("access_token"):
            params["access_token"] = config.access_token
    else: # url was passed in
        path = endpoint
    # generate path by combining params with the base url
    path += "?%s" % urllib.urlencode(params)
    return path

def request(url, method = "get", data = False, limit = config.max_api_pages):

    status = False
    req = urllib2.Request(url)
    if data:
        req = urllib2.Request(url, json.dumps(data))
    try: 
        req.get_method = lambda: method.upper()
        res = urllib2.urlopen(req)
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

    # decide whether to return now or continue recursing
    if limit == 0 or not "link" in res_headers.keys(): 
        return res_data, status

    next_url_match = re.match(r"<(?P<next_url>[^>]+)>; rel=\"next\"", res_headers['Link'])
    # if there isn't another url, return current response data
    if not next_url_match:
        return res_data, status

    # get the next urls data
    next_url = next_url_match.group("next_url")
    next_data, status = request(next_url, method, data, int(limit) - 1)

    # api call failed. Return whatever was returned - assume entire api call failed
    if not status:
        return next_data, status
    # successfully return everything
    return res_data + next_data, status


