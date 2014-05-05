import unittest
import config
from issue import Issue as I

class TestIssue(unittest.TestCase):

    def setUp(self):

        pass


    def test_new_issue(self):
        
        i = I.show_issue(config.repo_uri)
        
    def test_show_issue(self):

        i = I.show_issue(1, config.repo_uri)
        


if __name__ == "__main__":
    unittest.main()
