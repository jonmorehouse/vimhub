import unittest
import utils
import config
import github

class TestUtils(unittest.TestCase):

    def test_clean_data(self):

        data = {
            "key1": "",
            "key2": [],
            "no_key": "a",
            "key": "B"
        }
        _data = utils.clean_data(data, ["no_key"])
    
    def test_same_kwargs(self):

        kw1 = {"name": "jon", "last_name": "morehouse"}
        kw2 = {"last_name": "morehouse", "name": "jon"}
        self.assertTrue(utils.equal_dicts(kw1, kw2))

        kw2 = {"name": "joe"}
        self.assertFalse(utils.equal_dicts(kw1, kw2))

if __name__ == "__main__":
    unittest.main()

