import unittest
import utils
import config

class TestUtils(unittest.TestCase):
    

    def test_clean_data(self):

        data = {
            "key1": "",
            "key2": [],
            "no_key": "a",
            "key": "B"
        }
        _data = utils.clean_data(data, ["no_key"])

if __name__ == "__main__":
    unittest.main()

