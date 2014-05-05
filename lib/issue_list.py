import utils
import config
import git
import re

issue_list_hash = {} # hash objects per list ...

class IssueList():

    """
        Kwargs:
            state: default open
            label: none
            assignee: 
    """
    def __init__(self, path, **kwargs):

        self.path = utils.git_path(path)
        self._get_issues(**kwargs)
        if self.error_message:
            return
        self._generate_issue_list()

    @classmethod
    def get_issue_list(cls, cached = True, path = utils.git_path(), **kwargs):

        if not cached or not issue_list_hash.has_key(path):
            # no cache / no object - create issue_list
            issue_list_hash[path] = cls(path, **kwargs)
        return issue_list_hash[path]

    @classmethod
    def show_issue_list(cls, args):

        kwargs = {"state": "open"}
        # break up the pieces and then fill kwargs
        pieces = re.findall(r"[\w'=,]+", args)
        for piece in pieces: 
            # if no equal sign - assign to state
            if not "=" in piece:
                if piece in ("open", "closed", "state"):
                    kwargs["state"] = piece
                continue
            # user passed in custom params for github query
            p = tuple(re.split(r"[=]+", piece))
            kwargs[p[0]] = p[1]

        url = utils.github_url("repos/jonmorehouse/issues/issues", kwargs)
        

    @classmethod
    def open(line):
        issue_list = IssueList.get_issue_list() # get the issue list
    
    # private methods
    def _get_issues(self, **kwargs):

        if not kwargs.has_key("state") or not kwargs["state"] in ("open", "closed", "all"):
            kwargs["state"] = "open" 
        # if no upstream issues allowed and no issues locally - try to get upstream issues
        if not self.__try_get_issues(config.upstream_issues, **kwargs) and not config.upstream_issues:
            self.__try_get_issues(False, **kwargs)

    def __try_get_issues(self, upstream, **kwargs):

        # build out request url
        self.uri = git.get_uri(self.path, upstream)
        uri = "repos/%s/issues" % self.uri
        url = utils.github_url(uri, kwargs)
        # grab request data
        data, status = utils.github_request(url, "get")
        if not status:
            self.error_message = data
            self.data = None
        else:
            self.error_message = None
            self.data = data
        return status

    def _generate_issue_list(self):

        self.issues = [] # (number, title, @username, url)
        # this generates the visible list for issues that we will be handling
        for ih in self.data: # ih = issue_hash
            issue = (ih["number"], ih["title"], ih["user"]["login"], ih["url"])
            self.issues.append(issue) 


