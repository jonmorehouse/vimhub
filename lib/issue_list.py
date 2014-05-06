import utils
import config
import git
import re
import imp
import github
import issue
import __builtin__
import datetime

try:
    import vim
except ImportError as e:
    vim = False

il_hash = {} # hash objects by path

class IssueList():

    """
    Kwargs:
        repo: jonmorehouse/vim # required
        state: default open 
            label: none
            assignee: 
    """
    def __init__(self, **kwargs):
        
        if not kwargs.has_key("repo"):
            return 

        # initialize attrs
        self.kwargs = kwargs
        self.repo = kwargs.get("repo")
        self.buffer_name = "%s/issues" % self.repo
        il_hash[self.repo] = self

    @classmethod
    def show_issues(cls, *args, **kwargs):

        # normalize kwargs
        kwargs = utils.args_to_kwargs(args, kwargs)
        if not kwargs.get("repo"):
            kwargs["repo"] = github.repo_from_path()

        # case of now repo
        if not kwargs.get("repo") or not github.has_issues(kwargs.get("repo")):
            print "Unable to find repository. Please pass valid github uri or use from within a git directory"
            return

        # try to use cached il, if not, create a new one
        il = il_hash.get(kwargs.get("repo"))
        if not il or not utils.equal_dicts(il.kwargs, kwargs):
            il = cls(**kwargs)

        # update issue list
        il.update()
        
    @classmethod
    def open_issue(cls, args = True):

        # parse buffer and get uri
        uri = re.split(r"/issues$", vim.current.buffer.name)[0]
        # get issue_list uri
        issue_list = issue_list_uri_hash[uri]
        # parse current line to get issue number
        issue_number = re.findall(r"[\w']+", vim.current.line)[0]
        # open the issue
        issue.Issue.show_issue(issue_number)

    def draw(self):
    
        # get current buffer!
        b = utils.get_buffer(self.buffer_name)

        # append title
        b.append("## %s" % self.repo)
        b.append("")
        for i in self.issues:
            b.append("%s \"%s @%s\" %s " % (i[0], i[1], i[2], i[3]))
        # delete first line
        vim.command("1delete _")

    def update(self):
    
        self._get_issues()
        self.draw()
        self.map_buffer()

    def map_buffer(self):
        # enter into a new issue
        vim.command("map <buffer> <cr> :normal! 0<cr>:python IssueList.open_issue()<cr>")
        # refresh issues lists
        vim.command("map <buffer> s :python IssueList.show_issues(\"%s\")<cr>" % self.repo)
        # create a new issue for this repository
        vim.command("map <buffer> i :python Issue.open_issue(\"%s\", \"new\")<cr>" % self.repo)

    # private methods (non vim)
    def _get_issues(self, **kwargs):

        self.issues = [] #(number, title, @username, url)
        uri = "repos/%s/issues" % self.repo
        url = github.url(uri, kwargs)
        data, status = github.request(url, "get")
        # this generates the visible list for issues that we will be handling
        for ih in data: # ih = issue_hash
            issue = (ih["number"], ih["title"], ih["user"]["login"], ih["state"], ih["url"])
            self.issues.append(issue) 


