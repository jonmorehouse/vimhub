import utils
import config
import re
import git
import copy
import comment_list
import webbrowser

try:
    import vim
except ImportError as e:
    vim = False

issue_hash = {} # hash individual issues

class Issue:

    defaults = {
        "title": "",
        "assignee": "",
        "state": "open",
        "labels": [],
        "body": "",
    }

    def __init__(self, number, repo_uri):

        self.message = None
        self.repo_uri = repo_uri
        self.number = number
        self.issue_uri = "repos/%s/issues/%s" % (self.repo_uri, self.number) 
        self.comments = comment_list.CommentList(self.number, self.repo_uri,) 
        self._get_data()

    @classmethod
    def get_issue(cls, number = "new", repo_uri = None):

        if not repo_uri:
            repo_uri = git.get_uri()
        key = "%s/%s" % (repo_uri, str(number))

        if not issue_hash.has_key(key):
            issue_hash[key] = cls(number, repo_uri)

        return issue_hash[key]

    @classmethod
    def get_current_issue(self):

        return issue_hash[vim.current.buffer.name]

    @classmethod
    def open_issue(cls):
        
        i = cls.get_current_issue()
        if hasattr(i, "url"):
            webbrowser.open(i.url)
        i.map_buffer()

    @classmethod
    def save_issue(cls):
        
        i = cls.get_current_issue()
        i.position = vim.current.window.cursor
        i.parse() # parse the buffer
        i.comments.update() # update comments
        i.save() # push to the server
        i.post_hook()

    @classmethod
    def show_issue(cls, number = "new", repo_uri = None):

        if not repo_uri:
            repo_uri = git.get_uri()

        i = cls.get_issue(number, repo_uri)
        i.post_hook()
    
    @classmethod
    def toggle_state(cls, state = None):

        i = cls.get_current_issue()
        i.position = vim.current.window.cursor
        i.parse()
        i.change_state()
        i.save()
        i.post_hook()

    def change_state(self):

        if self.data["state"] == "open":
             self.data["state"] = "closed"
        else:
             self.data["state"] = "open"
        self.message = "State is now %s" % self.data["state"]
    
    def parse(self):
        # reset body
        self.data["body"] = ""

        # this is messy - convert to a matchgroup in the future
        for index, line in enumerate(vim.current.buffer[1:]):
            mg = re.match(r"# (?P<label>[^:]+): (?P<value>.*)", line)
            # handle normal attribute
            if mg:
                value = mg.group("value")
                label = mg.group("label").lower()
                if label in self.defaults.keys():
                    if self.data[label] == list:
                        self.data[label] = value.split(",")
                    else:
                        self.data[label] = value
            # handle error
            elif re.search(r"^## Comments Issue #%s" % self.number, line):
                # pass the comments to the other section
                self.comments.parse(vim.current.buffer[index+1:-1])
            else: 
                self.data["body"] += line

    def post_hook(self):

        self.draw()
        self.map_buffer()
        if hasattr(self, "position"):
            vim.command(str(self.position[0]))
            #vim.command("|%s" % str(self.position[1]))
    
    def map_buffer(self):
        # autocommand to call on post save ...
        vim.command("map <buffer> s :python issue.Issue.save_issue()<cr>")
        # toggle the state of the current issue
        vim.command("map <buffer> c :python issue.Issue.toggle_state()<cr>")
        # hit enter to browse the current url
        vim.command("map <buffer> <cr> :normal! 0<cr>:python issue.Issue.open_issue()<cr>")

    def draw(self):
    
        self.buffer_name = "%s/%s" % (self.repo_uri, self.number)
        b = utils.get_buffer(self.buffer_name) 
        vim.command("1,$d")

        # print out issue
        b.append("## %s # %s" % (self.repo_uri, self.number))
        b.append("")

        # iterate through all keys that aren't body
        keys = self.data.keys()
        keys.remove("body")
        for key in keys:
            value = self.data[key]
            if type(value) == list:
                value = ",".join(value)
            b.append("# %s: %s" % (key.capitalize(), value))

        # print out body if applicable
        if self.data.has_key("body"):
            b.append("")
            b.append(self.data["body"])
        
        # now we need to print the comments
        self.comments.draw(b)

        # remove leading line
        vim.command("1delete _")

    def save(self):

        if self.number == "new":
            self._create_issue()
        else: 
           self._save_issue() 

    def _get_data(self):

        self.data = copy.deepcopy(self.defaults)

        # get issue from github api if not new
        if not self.number == "new":
            data, status = utils.github_request(utils.github_url(self.issue_uri))
            if not status:
                self.message = data
                return

            # issue was successfully requested
            for key in self.defaults.keys() + ["assignee", "user"]:
                if key in ("assignee", "user"):
                    self.data[key] = data[key]["login"]
                elif key == "labels":
                    self.data[key] = [str(label["name"]) for label in data[key]]
                else:
                    self.data[key] = data[key]

            # grab the browse url 
            self.url = data["html_url"]

    def _create_issue(self):
        # create issue on the server
        uri = "repos/%s/issues" % self.repo_uri
        url = utils.github_url(uri)
        data = utils.clean_data(copy.deepcopy(self.data), ["state"])
        if not data:
            self.message = "Issue not ready yet..."
            return
        data, status = utils.github_request(url, "post", data)
        if not status:
            self.message = data
            return 

        # update attributes as needed for object
        self.number = str(data["number"])
        self.data["user"] = data["user"]["login"]
        self.url = data["html_url"]
        self.issue_uri = "repos/%s/issues/%s" % (self.repo_uri, self.number)
        self.comments.number = self.number

        # clean up hash
        del issue_hash["%s/%s" % (self.repo_uri, "new")]
        issue_hash["%s/%s" % (self.repo_uri, self.number)] = self
        # delete the old buffer that we don't need any more
        vim.command("bdelete")

    def _save_issue(self):

        # get ready for the patch operation
        url = utils.github_url(self.issue_uri)
        data = utils.clean_data(copy.deepcopy(self.data), ["number", "user"])
        data, status = utils.github_request(url, "patch", data)

