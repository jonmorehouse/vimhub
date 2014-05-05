import unittest
import config
from issue_list import IssueList as IL

class TestIssueList(unittest.TestCase):

    def setUp(self):

        pass
    
    def test_issue_list(self):
        
        kwargs = {"state": "open"}
        il = IL(config.test_repo_path, **kwargs)
        pass
    
    def test_get_issue_list(self):

        # this should return a valid issue list for this project ...
        obj = IL.get_issue_list(True, config.test_repo_path)
        objCached = IL.get_issue_list(True, config.test_repo_path)
        objUncached = IL.get_issue_list(False, config.test_repo_path)
        # check caching works properly
        self.assertTrue(obj == objCached)
        #check uncaching works correctly
        self.assertFalse(obj == objUncached)

    def test_show_issue_list(self):

        args = "all label=bug,enhancement"
        obj = IL.show_issue_list(args) # if in vim then we should also print the elements as needed!

if __name__ == "__main__":
    unittest.main()

