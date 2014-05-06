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
    def __init__(self, path = None, **kwargs):
        
        self.path = path
        if not self.path:
            self.path = utils.git_path(path)
        # grab all issues
        self._get_issues(**kwargs)
        if self.message:
            return
        self._generate_issue_list()
        issue_list_uri_hash[self.uri] = self

    @classmethod
    def get_issue_list(cls, path = None, cached = True, **kwargs):

        if not path:
            path = utils.git_path()

        if cached and issue_list_hash.has_key(path):
            return issue_list_hash[path]
        
        il = cls(path, **kwargs)
        issue_list_hash[path] = il
        return il
    
    @classmethod
    def show_issue_list(cls, args = None, path = None):

        if not path:
            path = utils.git_path()

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
        il = cls.get_issue_list(path, False, **kwargs)
        il.buffer_name = "%s/issues" % il.uri
        il.draw()
        il.map_buffer()
        
    @classmethod
    def issue_list_selection(cls, args = True):

        # parse buffer and get uri
        uri = re.split(r"/issues$", vim.current.buffer.name)[0]
        # get issue_list uri
        issue_list = issue_list_uri_hash[uri]
        # parse current line to get issue number
        issue_number = re.findall(r"[\w']+", vim.current.line)[0]
        # open the issue
        issue.Issue.show_issue(issue_number)

    def draw(self):
    
        if not vim: 
            return

        # get current buffer!
        b = utils.get_buffer(self.buffer_name)
        if self.message: # handle fatal error
            b.append(self.message)
            return 

        # append title
        b.append("## %s" % self.uri)
        b.append("")
        for i in self.issues:
            b.append("%s \"%s @%s\" %s " % (i[0], i[1], i[2], i[3]))
        # delete first line
        vim.command("1delete _")

    def map_buffer(self):
        
        if not vim: 
            return

        # enter into a new issue
        vim.command("map <buffer> <cr> :normal! 0<cr>:python IssueList.issue_list_selection()<cr>")
        # refresh issues lists
        vim.command("map <buffer> s :python IssueList.show_issue_list()<cr>")
        # create a new issue
        vim.command("map <buffer> i :python Issue.open_issue()<cr>")
        vim.command("map <buffer> a :python IssueList.open_issue()<cr>")

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
            self.message = data
            self.data = None
        else:
            self.message = None
            self.data = data
        return status

    def _generate_issue_list(self):

        self.issues = [] # (number, title, @username, url)
        # this generates the visible list for issues that we will be handling
        for ih in self.data: # ih = issue_hash
            issue = (ih["number"], ih["title"], ih["user"]["login"], ih["state"], ih["url"])
            self.issues.append(issue) 

