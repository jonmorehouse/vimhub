import unittest
import github

class TestGithub(unittest.TestCase):

    def setUp(self):

        pass


    def test_user(self):

        u = github.user()
        u1 = github.user()

        self.assertTrue(u)
        # make sure hash works
        self.assertTrue(u is u1)
    
    def test_has_issues(self):

        self.assertTrue(github.has_issues(("jonmorehouse/vim-github")))
        self.assertFalse(github.has_issues(("jonmorehouse/github-issues.vim")))

    def test_time_from_string(self):

        to = github.time(github.user().get("updated_at"))

if __name__ == "__main__":
    unittest.main()
