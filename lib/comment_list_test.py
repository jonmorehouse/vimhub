import unittest
import config
from comment_list import CommentList as CL

class TestCommentList(unittest.TestCase):

    def setUp(self):

        pass

    def test_comment_list(self):

        c = CL("1", config.repo_uri)
         

if __name__ == "__main__":
    unittest.main()
