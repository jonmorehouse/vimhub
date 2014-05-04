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

    #def test_github_request(self):

        #response, status = utils.github_request(self.url)
        #self.assertTrue(response)
        #self.assertTrue(status)

    def test_github_paging_request(self):

        url = utils.github_url("repos/homebrew/homebrew/issues")
        response, status = utils.github_request(url)


if __name__ == "__main__":
    unittest.main()

