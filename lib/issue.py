import utils
import config
import re
import git
import copy
import comment_list
import webbrowser
import github

try:
    import vim
except ImportError as e:
    vim = False

i_hash = {} # hash individual issues

class Issue:

    defaults = {
        "title": "",
        "assignee": "",
        "milestone": "",
        "state": "open",
        "labels": [],
        "body": "",
    }

    def __init__(self, **kwargs):
        
        # set defaults for class
        if not Issue.defaults.get("assignee"):
            Issue.defaults["assignee"] = utils.github.user()["login"],
        self.repo = kwargs.get("repo")
        self.number = kwargs.get("number")
        self.issue_uri = "repos/%s/issues/%s" % (self.repo, self.number) 
        self.comments = comment_list.CommentList(self.number, self.repo) 
        self._get_data()

    @classmethod
    def open(cls, *args):

        i = cls._issue_from_args(*args)
        if not i or not i.repo:
            print "Not a valid repository or issue. Please try again or consult help pages"
            return
        i.post_hook()

    @classmethod
    def browse(cls, *args):
        
        i = cls._issue_from_args(*args)
        if hasattr(i, "url"):
            webbrowser.open(i.url)
        i.map_buffer()

    @classmethod
    def save(cls):
        
        i = cls._issue_from_buffer()
        if not i:
            print "Error has occurred. Issue was not found. Please report an issue on github"
            return

        # parse the uri from this issue
        i.position = vim.current.window.cursor
        i.parse() # parse the buffer
        i.update() # push to the server
        i.post_hook()

    @classmethod
    def toggle_state(cls):

        i = cls._issue_from_buffer()
        i.position = vim.current.window.cursor
        i.parse() # parse current buffer to correct location
        i.change_state()
        i.update()
        i.post_hook()

    @classmethod
    def _issue_from_args(cls, *args, **kwargs):
    
        kwargs = utils.args_to_kwargs(args, kwargs)

        if not kwargs.get("args") or len(kwargs.get("args")) == 0:
            kwargs["number"] = "new"
        else:
            kwargs["number"] = kwargs.get("args")[0]
            del kwargs["args"]
        
        key = "%s/%s" % (kwargs.get("repo"), kwargs.get("number"))
        if not i_hash.has_key(key):
            i_hash[key] = cls(**kwargs)
        return i_hash.get(key)

    @classmethod
    def _issue_from_buffer(cls):

        # bname corresponds to to the issue hash key 
        bname = vim.current.buffer.name

        # check to make sure the correct pieces are here
        mg = re.match(r"(?P<user>.*)/(?P<repo>.*)/(?P<issue>.*)", bname)
        if not mg:
            return None
        return i_hash.get(bname)
        

    def change_state(self):

        if self.data["state"] == "open":
             self.data["state"] = "closed"
        else:
             self.data["state"] = "open"
    
    def parse(self):
        # reset body
        self.data["body"] = []

        # this is messy - convert to a matchgroup in the future
        for index, line in enumerate(vim.current.buffer[1:]):
            mg = re.match(r"# (?P<label>[^:]+): (?P<value>.*)", line)
            # handle normal attribute
            if mg:
                value = mg.group("value")
                label = mg.group("label").lower()
                if label in self.defaults.keys():
                    if type(self.defaults[label]) == list:
                        self.data[label] = value.split(",")
                    else:
                        self.data[label] = value
            # handle error
            elif re.search(r"^## Comments Issue #%s" % self.number, line):
                # pass the comments to the other section
                self.comments.parse(vim.current.buffer[index+1:-1])
                break
            else: 
                self.data["body"].append(line)

        self.data["body"] = utils.trim_lines(self.data["body"])

    def post_hook(self):

        self.draw()
        self.map_buffer()
        if hasattr(self, "position"):
            vim.command(str(self.position[0]))
            #vim.command("|%s" % str(self.position[1]))
    
    def map_buffer(self):
        # autocommand to call on post save ...
        vim.command("map <buffer> s :python issue.Issue.save()<cr>") # uses current buffer name
        # toggle the state of the current issue
        vim.command("map <buffer> cc :python issue.Issue.toggle_state()<cr>") # uses current buffer name
        # hit enter to browse the current url
        vim.command("map <buffer> <cr> :normal! 0<cr>:python issue.Issue.browse(\"%s\", \"%s\")<cr>" % (self.repo, self.number)) # doesn't use current buffer name

    def draw(self):
    
        self.buffer_name = "%s/%s" % (self.repo, self.number)
        b = utils.get_buffer(self.buffer_name) 
        vim.command("1,$d")
        vim.command("set filetype=markdown")

        # print out issue
        b.append("## %s # %s" % (self.repo, self.number))
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
        if self.data.has_key("body") and self.data["body"]:
            for line in self.data["body"].splitlines():
                b.append(line)
        
        # now we need to print the comments
        self.comments.draw(b)
        # remove leading line
        vim.command("1delete _")

    def update(self):

        if self.number == "new":
            self._create_issue()
        else: 
           self._save_issue() 

    def _get_data(self):

        self.data = copy.deepcopy(self.defaults)

        # get issue from github api if not new
        if not self.number == "new":
            data, status = github.request(github.url(self.issue_uri))
            if not status:
                utils.log(data)
                return

            # issue was successfully requested
            for key in self.defaults.keys() + ["assignee", "user"]:
                # github will return None
                if key in ("assignee", "user") and data.get(key):
                    self.data[key] = data[key]["login"]
                elif key == "labels":
                    self.data[key] = [str(label["name"]) for label in data[key]]
                elif key == "milestone" and data.get("milestone"):
                    self.data[key] = data[key]["title"]
                elif data.get(key):
                    self.data[key] = data[key]

            # grab the browse url 
            self.url = data["html_url"]

    def _create_issue(self):
        # create issue on the server
        uri = "repos/%s/issues" % self.repo
        url = github.url(uri)
        data = utils.clean_data(copy.deepcopy(self.data), ["state"])
        if not data or len(data.keys()) == 0:
            utils.log("New issues require title/body")
            return
        data, status = github.request(url, "post", data)
        if not status:
            utils.log(data)
            return 

        # update attributes as needed for object
        self.number = str(data["number"])
        self.data["user"] = data["user"]["login"]
        self.url = data["html_url"]
        self.issue_uri = "repos/%s/issues/%s" % (self.repo, self.number)
        self.comments.number = self.number

        # clean up hash
        del i_hash["%s/%s" % (self.repo, "new")]
        i_hash["%s/%s" % (self.repo, self.number)] = self

        # delete the old buffer that we don't need any more
        vim.command("silent new")
        vim.command("bdelete %s" % self.buffer_name)

    def _save_issue(self):

        # get ready for the patch operation
        url = github.url(self.issue_uri)
        data = utils.clean_data(copy.deepcopy(self.data), ["number", "user", "labels"])
        data, status = github.request(url, "patch", data)


