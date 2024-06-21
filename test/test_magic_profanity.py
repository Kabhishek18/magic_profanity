
import unittest
from magic_profanity.magic_profanity import ProfanityFilter

class TestMagicProfanity(unittest.TestCase):
    def setUp(self):
        self.profanity_filter = ProfanityFilter()
        # Load custom words for testing if necessary
        # self.profanity_filter.load_censor_words(["badword1", "badword2"])

    def test_contains_profanity(self):
        self.assertTrue(self.profanity_filter.has_profanity("This sentence contains a fuck"))
        self.assertTrue(self.profanity_filter.has_profanity("This sentence contains a fucker"))

    def test_censor(self):
        self.profanity_filter.add_custom_words(["badword1", "badword4"])
        censored_text = self.profanity_filter.censor_text("This sentence contains a badword1")
        self.assertEqual(censored_text, "This sentence contains a ****")

    def test_add_censor_words(self):
        self.profanity_filter.add_custom_words(["badword3", "badword4"])
        censored_text = "This sentence contains a badword4"

        self.assertTrue(self.profanity_filter.has_profanity(censored_text))

    def tearDown(self):
        # Clean up if necessary
        pass

if __name__ == "__main__":
    unittest.main()
