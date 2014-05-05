import utils
import config
import git
import re
import imp
import issue
import __builtin__
try:
    import vim
except ImportError as e:
    vim = False

issue_list_hash = {} # hash objects by path
issue_list_uri_hash = {} # hash objects by uri

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
        issue_list_uri_hash[self.uri] = self

    @classmethod
    def get_issue_list(cls, cached = True, path = utils.git_path(), **kwargs):

        if not cached or not issue_list_hash.has_key(path):
            # no cache / no object - create issue_list
            issue_list_hash[path] = cls(path, **kwargs)
        return issue_list_hash[path]
    
    @classmethod
    def show_issue_list(cls, args = None):

        kwargs = {"state": "open"}
        if args:
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

        # get the issue list - this should always refresh in case there are new issues (and because it shouldn't, in theory be called that much ...)
        issue = cls.get_issue_list(False, **kwargs)
        issue.buffer_name = "%s/issues" % issue.uri
        issue.draw() # draw the buffer
        issue.register_mappings() # register vim_mappings
        
    @classmethod
    def issue_list_selection(cls, args = True):

        # parse buffer and get uri
        uri = re.split(r"/issues$", vim.current.buffer.name)[0]
        # get issue_list uri
        issue_list = issue_list_uri_hash[uri]
        # parse current line to get issue number
        issue_number = re.findall(r"[\w']+", vim.current.line)[0]
        # open the issue
        issue.Issue.show(issue_number)

    def draw(self):
    
        if not vim: return

        # get current buffer!
        b = utils.get_buffer(self.buffer_name)
        # append title
        b.append("## %s" % self.uri)
        b.append("")
        for i in self.issues:
            b.append("%s \"%s @%s\" %s " % (i[0], i[1], i[2], i[3]))
        # delete first line
        vim.command("1delete _")

    def register_mappings(self):
        
        if not vim: return
        # enter into a new issue
        vim.command("map <buffer> <cr> :normal! 0<cr>:python issue_list.IssueList.issue_list_selection()<cr>")
        # refresh issues lists
        vim.command("map <buffer> s :python issue_list.IssueList.show_issue_list()<cr>")
        # create a new issue
        vim.command("map <buffer> i :python issue_list.IssueList.test()<cr>")
        vim.command("map <buffer> a :python issue_list.IssueList.test()<cr>")

    # private methods (non vim)
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
            issue = (ih["number"], ih["title"], ih["user"]["login"], ih["state"], ih["url"])
            self.issues.append(issue) 


