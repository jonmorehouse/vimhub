import utils
import config
import re
import git

try:
    import vim
except ImportError as e:
    vim = False

issue_hash = {} # hash individual issues

class Issue:

    def __init__(uri, number = "new"):

        pass

    @classmethod
    def save_issue():

        pass

    @classmethod
    def show_issue(number = "new", uri = git.get_uri()):
        print uri
        # download 

    def draw():
        if not vim: return




