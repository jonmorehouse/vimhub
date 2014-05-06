import unittest
import config
from issue import Issue as I

class TestIssue(unittest.TestCase):

    def setUp(self):

        pass

    def test_issue_from_args(self):

        I.issue_from_args(["jonmorehouse/repo/1"])



if __name__ == "__main__":
    unittest.main()
