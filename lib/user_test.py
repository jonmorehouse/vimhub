import unittest
import config
import user


class TestUser(unittest.TestCase):

    def test_user_get_login(self):

        u = user.get_login()

if __name__ == "__main__":
    unittest.main()
