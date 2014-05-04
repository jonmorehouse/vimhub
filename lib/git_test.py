import unittest
import git

class TestGit(unittest.TestCase):

    def setUp(self):

        pass

    def test_get_remotes(self):

        remotes = git.get_remotes(".")

    def test_get_remote(self):

        repo_uri = git.get_remote(".")
        repo_uri = git.get_remote(".")

    def test_get_uri(self):

        repo_uri = git.get_uri(".")
        repo_uri = git.get_uri(".")

if __name__ == "__main__":
    unittest.main()


