import unittest
import github

class TestGithub(unittest.TestCase):

    def setUp(self):
    
        self.endpoint = "repos/jonmorehouse/issues/issues"
        self.params = {"state": "all"}
        self.url = github.url(self.endpoint, self.params)

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

    def test_github_url(self):

        # test a path
        path = github.url(self.endpoint, self.params)
        self.assertTrue(len(path) > 0)

    def test_github_request(self):

        response, status = github.request(self.url)
        self.assertTrue(response)
        self.assertTrue(status)

    def test_github_paging_request(self):

        url = github.url("repos/jaxbot/github-issues.vim/issues", self.params)
        data, status = github.request(url)
        self.assertTrue(data)
        self.assertTrue(status)

    def test_github_post_request(self):

        defaults = {
            "title": "Title",
        }
        url = github.url("repos/jonmorehouse/issues/issues", self.params)
        data, status = github.request(url, "post", defaults) 

if __name__ == "__main__":
    unittest.main()
