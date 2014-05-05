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

        if number == "new":
            self._new()
        else:
            self._get_issue()

    @classmethod
    def save_issue(cls):
        
        pass

    @classmethod
    def show_issue(cls, number = "new", uri = git.get_uri()):

        pass

    def _get_issue(number):

        pass












