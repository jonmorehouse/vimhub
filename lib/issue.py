import utils
import config
import re
import git
import copy
import comment_list

try:
    import vim
except ImportError as e:
    vim = False

issue_hash = {} # hash individual issues

class Issue:

    defaults = {
        "title": "",
        "number": "new",
        "assignee": "",
        "state": "open",
        "labels": [],
        "user": {
            "login": ""
        }
    }

    def __init__(self, number, repo_uri):

        self.error_message = None
        self.repo_uri = repo_uri
        self.number = number
        self.issue_uri = "repos/%s/issues/%s" % (self.repo_uri, self.number) 
        self.comments = None
        self._get_issue_data()
        self._get_comments()

    @classmethod
    def get_issue(cls, number = "new", uri = "test"):

        # grab the issue
        if issue_hash.has_key(number):
            i = issue_hash[number]
        else:
            i = cls(number, uri)
        return i

    @classmethod
    def save_issue(cls):
        
        print "SAVE"

    @classmethod
    def show_issue(cls, number = "new", repo_uri = "test"):

        i = cls.get_issue(number, repo_uri)
        i.draw()

    def update_from_string(content):

        # loop through string and update the internal hash
        pass

    def map_buffer(self):

        pass

    def draw(self):
    
        self.buffer_name = "%s/%s" % (self.repo_uri, self.number)
        b = utils.get_buffer(self.buffer_name) 
        vim.command("1,$d")

        # handle if an error exists
        if self.error_message:
            b.append(error_message)
            return

        # print out issue
        b.append("## %s" % self.repo_uri)
        b.append("")

        # print out keys
        for key in self.defaults.keys():
            value = self.data[key]
            # if key is a user - print the key "login"
            if key in ("assignee", "user"):
                value = self.data[key]["login"]
            b.append("# %s: %s" % (key.capitalize(), value))

        # print out body if applicable
        if self.data.has_key("body"):
            b.append("")
            b.append(self.data["body"])
        
        # now we need to print the comments
        if self.comments:
            self.comments.draw(b)

        # remove leading line
        vim.command("1delete _")

    def _get_issue_data(self):

        self.data = copy.deepcopy(self.defaults)
        # get issue from github api if not new
        if not self.number == "new":

            data, status = utils.github_request(utils.github_url(self.issue_uri))
            if not status:
                self.error_message = data
                return
            self.data.update(data)

    
    def _get_comments(self):

        if self.data.has_key("comments") and self.data["comments"] > 0: 
            self.comments = comment_list.CommentList(self.repo_uri, self.number)
    
    def _create_issue(self):

        pass # save a new issue

    def _save_issue(self):

        pass















