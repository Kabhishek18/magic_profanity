
import unittest
from magic_profanity.magic_profanity import MagicProfanity

class TestMagicProfanity(unittest.TestCase):
    def setUp(self):
        self.profanity_filter = MagicProfanity()
        # Load custom words for testing if necessary
        # self.profanity_filter.load_censor_words(["badword1", "badword2"])

    def test_contains_profanity(self):
        self.assertTrue(self.profanity_filter.contains_profanity("This sentence contains a badword1"))
        self.assertTrue(self.profanity_filter.contains_profanity("This sentence contains a BadWord2"))

    def test_censor(self):
        censored_text = self.profanity_filter.censor("This sentence contains a badword1")
        self.assertEqual(censored_text, "This sentence contains a *********")

    def test_add_censor_words(self):
        self.profanity_filter.add_censor_words(["badword3", "badword4"])
        self.assertTrue(self.profanity_filter.contains_profanity("This sentence contains a BadWord3"))
        self.assertTrue(self.profanity_filter.contains_profanity("This sentence contains a badword4"))

    def tearDown(self):
        # Clean up if necessary
        pass

if __name__ == "__main__":
    unittest.main()
