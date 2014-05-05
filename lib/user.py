import utils
import config

_user = {}

def get_login():

    u = get_user()
    return u["login"]


def get_user():

    global _user
    if len(_user.keys()) > 0:
        return _user

    url = utils.github_url("user")
    data, status = utils.github_request(url)
    if not status:
        print data

    # cache this hash
    _user = data
    return _user
    
