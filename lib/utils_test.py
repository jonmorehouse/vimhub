import unittest
import utils
import config

class TestUtils(unittest.TestCase):
    
    def setUp(self):
    
        self.endpoint = "repos/jonmorehouse/issues/issues"
        self.params = {"state": "all"}
        self.url = utils.github_url(self.endpoint, self.params)

    def test_git_path(self):
    
        path = utils.git_path(".")

    def test_github_url(self):

        # test a path
        path = utils.github_url(self.endpoint, self.params)
        self.assertTrue(len(path) > 0)

    def test_github_request(self):

        response, status = utils.github_request(self.url)
        self.assertTrue(response)
        self.assertTrue(status)

    def test_github_paging_request(self):

        url = utils.github_url("repos/jaxbot/github-issues.vim/issues", self.params)
        data, status = utils.github_request(url)
        self.assertTrue(data)
        self.assertTrue(status)

    def test_github_post_request(self):

        defaults = {
            "title": "Title",
        }
        url = utils.github_url("repos/jonmorehouse/issues/issues", self.params)
        data, status = utils.github_request(url, "post", defaults) 

    def test_clean_data(self):

        data = {
            "key1": "",
            "key2": [],
            "no_key": "a",
            "key": "B"
        }
        _data = utils.clean_data(data, ["no_key"])
        print _data


if __name__ == "__main__":
    unittest.main()

