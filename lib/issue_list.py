import utils
import config
import copy
import git
import re
import imp
import github
from issue import Issue
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
        if not il or not utils.equal_dicts(il.kwargs, kwargs) and not kwargs.get("update"):
            il = cls(**kwargs)

        # update issue list
        il.update()

    @classmethod
    def issue(cls, *args, **kwargs):

        # remap old buffer
        # parse buffer and get uri
        repo = re.split(r"/issues$", vim.current.buffer.name)[0]
        args = list(args)
        args.append(repo)

        # generate the issue to pass on
        if kwargs.get("issue"):
            args.append(kwargs.get("issue"))
        else:
            ma = re.findall(r"[\w']+", vim.current.line)
            if not ma:
                return
            args.append(ma[0].replace(".", ""))

        # call the method
        getattr(Issue, kwargs.get("method"))(*args)

    def draw(self):
    
        # get current buffer!
        b = utils.get_buffer(self.buffer_name)

        # set to markdown syntax for now
        vim.command("set filetype=markdown")

        # append title
        b.append("## %s" % self.repo)
        b.append("")
        
        for i in self.issues:
            issue_string = "%s. \"%s\" " % (i[0], i[1])

            if len(i[5]) > 0:
                 issue_string += "#%s " % ",".join(i[5])
            
            if not (i[2] == github.user()["login"]):
                issue_string += "@%s " % i[2]
            if not (i[3] == "open"):
                issue_string += i[3]
            
            # add labels if they exist
            b.append(issue_string)

        # delete first line
        vim.command("1delete _")

    def update(self):
    
        self._get_issues(**self.kwargs)
        self.draw()
        self.map_buffer()

    def map_buffer(self):
        # refresh issues lists
        vim.command("map <buffer> s :python IssueList.show_issues(\"%s\", update=True)<cr>" % self.repo)
        # open issue
        vim.command("map <buffer> <cr> :normal! 0<cr>:python IssueList.issue(method=\"open\")<cr>")
        # browse issue (online)
        vim.command("map <buffer> o :python IssueList.issue(method=\"browse\")<cr>")
        # create new issue
        vim.command("map <buffer> i :python IssueList.issue(method=\"open\", issue=\"new\")<cr>")

    # private methods (non vim)
    def _get_issues(self, **kwargs):

        self.issues = [] #(number, title, @username, url)
        uri = "repos/%s/issues" % self.repo
        # prepare kwargs for getting the correct issues
        kwargs = utils.clean_data(copy.deepcopy(kwargs), ("repo"), (("label", "labels"),))
        url = github.url(uri, kwargs)
        data, status = github.request(url, "get")
        # this generates the visible list for issues that we will be handling
        for ih in data: # ih = issue_hash
            issue = (ih["number"], ih["title"], ih["user"]["login"], ih["state"], ih["url"], [l.get("name") for l in ih["labels"]])
            self.issues.append(issue) 

