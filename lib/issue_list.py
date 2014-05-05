import utils

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
        if not kwargs.has_key("state") or not kwargs["state"] in ("open", "closed", "all"):
            kwargs["state"] = "open" 
        self._get_issues(**kwargs)
        # update the hash
        issue_list_hash[self.path] = self

    @classmethod
    def get_issue_list(args, cached = False):

        path = utils.git_path()
        # handle cached version etc
        if cached and issue_list_hash.has_key(path):
            return issue_list_hash[path]

        # no cache / no object - create issue_list



    @classmethod
    def open(line):

        pass
    
    def update():

        pass 

    def view(self):

        # print methods
        # create mappings
        pass


