import config
import utils
import time
import re
import user
from collections import OrderedDict

try:
    import vim
except ImportError as e:
    vim = False

class CommentList(object):

    def __init__(self, number, repo_uri):

        self.login = user.get_login()
        self.message = ""
        self.editable_comments = {}
        self.comments = OrderedDict()
        self.user_comments = [] # list of ids that will get updated each time
        self.repo_uri = repo_uri
        self.number = number
        self._get_comments()

    def update(self):

        self.comments = {}
        self._get_comments()

    # pass in a buffer
    def draw(self, b):

        b.append("")
        b.append("## Comments Issue #%s" % self.number)
        for _id, comment in self.comments.iteritems():
            b.append("## @%s at %s %s" % (comment["user"], comment["time"], comment["id"]))
            for line in comment["body"]:
                b.append(line)
            b.append("")

        # draw out new id!
        b.append("## New Comment")
        b.append("")
        b.append("")

    def parse(self, lines):

        comment = {"body": []}
        for line in lines[1:]:
            # skip any empty lines
            if re.search(r"^\s*$", line):
                continue
            cmg = re.match(r"## @(?P<login>[^ at]+) (?P<date>.*) (?P<id>.*)", line)
            if cmg: #start parsing a group
                self._process_comment(comment)
                comment = {"login": cmg.group("login"), "id": cmg.group("id"), "body": []}
            elif re.search(r"^## New Comment", line):
                self._process_comment(comment)
                comment = {"login": self.login, "id": "new", "body": []}
            else:
                comment["body"].append(line.strip())

        self._process_comment(comment)

    @property
    def number(self):
        return self._number

    @number.setter # issue number
    def number(self, new_number):
        
        self._number = new_number
        self.uri = "repos/%s/issues/%s/comments" % (self.repo_uri, self._number)

    def _process_comment(self, comment):

        if not comment.has_key("login") and not comment.has_key("id") or not comment["login"] == self.login or not comment.has_key("body"):
            return

        # create a new comment
        if comment["id"] == "new": 
            if len(comment["body"]) > 0:
                self._create_comment("\n".join(comment["body"]))
                return
            else:
                return

        if comment.has_key("id") and len(comment["body"]) == 0: 
            self._delete_comment(comment["id"])
            return

        # get comparison working so issues don't make requests as well
        if comment["id"] in self.editable_comments:
            self._edit_comment(comment["id"], "\n".join(comment["body"]))

    def _edit_comment(self, cid, body):

        pass
        #data, status = utils.github_request(url, "patch", {"body": body})

    def _delete_comment(self, cid):

        url = utils.github_url(self.comments[cid]["url"])
        del self.comments[cid]
        data, status = utils.github_request(url, "delete")

    def _create_comment(self, body):

        url = utils.github_url(self.uri)
        data, status = utils.github_request(url, "post", {"body": body})
        self._cache_comment(data)
    
    def _cache_comment(self, comment):

        print comment
        c =  {
            "user": comment["user"]["login"],
            "body": comment["body"].splitlines(),
            "time": comment["updated_at"],
            "id": str(comment["id"]),
            "url": comment["url"]
        }
        self.comments[c["id"]] = c

    def _get_comments(self):

        if self.number == "new":
            return

        # make the request as needed
        url = utils.github_url(self.uri) 
        data, status = utils.github_request(url, "get")        
        
        if not status:
            self.message = data
            return
        for comment in data:
            self._cache_comment(comment)

