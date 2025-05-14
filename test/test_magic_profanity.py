# test/test_magic_profanity.py
import unittest
from magic_profanity.magic_profanity import ProfanityFilter
from magic_profanity.enhancement import TextEnhancer
from magic_profanity.sentiment import SentimentAnalyzer


class TestMagicProfanity(unittest.TestCase):
    def setUp(self):
        # Basic profanity filter
        self.basic_filter = ProfanityFilter()

        # Filter with sentiment analysis
        self.sentiment_filter = ProfanityFilter(
            enable_sentiment=True,
            sentiment_options={
                'custom_threshold': {'positive': 0.1, 'negative': -0.1},
                'preprocess_text': True
            }
        )

        # Filter with all features
        self.full_filter = ProfanityFilter(
            enable_sentiment=True,
            sentiment_options={
                'custom_threshold': {'positive': 0.1, 'negative': -0.1},
                'preprocess_text': True
            },
            enable_enhancement=True
        )

        # Test texts
        self.clean_text = "This product is really amazing! I love how well it works."
        self.profane_text = "This damn product is terrible. I hate it."
        self.mixed_text = "The interface is amazing but the performance sucks sometimes."

    def test_basic_functionality(self):
        """Test the basic profanity filtering functionality."""
        # Add "sucks" to the profanity list for testing
        self.basic_filter.add_custom_words(["sucks"])

        # Test profanity detection
        self.assertFalse(self.basic_filter.has_profanity(self.clean_text))
        self.assertTrue(self.basic_filter.has_profanity(self.profane_text))
        self.assertTrue(self.basic_filter.has_profanity(self.mixed_text))

        # Test censoring
        censored_text = self.basic_filter.censor_text(self.profane_text)
        self.assertNotEqual(censored_text, self.profane_text)
        self.assertFalse("damn" in censored_text)

        # Test custom words
        self.basic_filter.add_custom_words(["amazing"])
        self.assertTrue(self.basic_filter.has_profanity(self.clean_text))

        # Reset for further tests
        self.basic_filter = ProfanityFilter()


    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality."""
        # Ensure sentiment analyzer is properly initialized
        self.assertIsNotNone(self.sentiment_filter.sentiment_analyzer)

        # Test basic sentiment analysis
        analysis1 = self.sentiment_filter.analyze_text(self.clean_text)
        analysis2 = self.sentiment_filter.analyze_text(self.profane_text)

        # Verify structure of analysis output
        self.assertIn('sentiment', analysis1)
        self.assertIn('classification', analysis1['sentiment'])
        self.assertIn('scores', analysis1['sentiment'])

        # Verify sentiment classifications
        self.assertEqual(analysis1['sentiment']['classification'], 'positive')
        self.assertEqual(analysis2['sentiment']['classification'], 'negative')

        # Test detailed sentiment analysis
        detailed = self.sentiment_filter.analyze_text(self.mixed_text, detailed=True)
        self.assertIn('confidence', detailed['sentiment'])
        self.assertIn('emotion_indicators', detailed['sentiment'])

    def test_enhancement_suggestions(self):
        """Test text enhancement functionality."""
        # Ensure text enhancer is properly initialized
        self.assertIsNotNone(self.full_filter.text_enhancer)

        # Test enhancement suggestions
        analysis = self.full_filter.analyze_text(self.profane_text)

        # Verify structure of enhancement suggestions
        self.assertIn('enhancement_suggestions', analysis)
        self.assertIn('politeness_improvements', analysis['enhancement_suggestions'])
        self.assertIn('clarity_improvements', analysis['enhancement_suggestions'])
        self.assertIn('tone_improvements', analysis['enhancement_suggestions'])
        self.assertIn('overall_recommendations', analysis['enhancement_suggestions'])

        # Check for specific suggestions
        politeness = analysis['enhancement_suggestions']['politeness_improvements']
        self.assertTrue(any('damn' in suggestion['original'].lower() for suggestion in politeness))

        # Test with a more complex text
        complex_text = "I always hate when people never respond to my emails. This is stupid and terrible!"
        complex_analysis = self.full_filter.analyze_text(complex_text)

        # Check for clarity improvements
        clarity = complex_analysis['enhancement_suggestions']['clarity_improvements']
        self.assertTrue(
            any('always' in suggestion['original'].lower() for suggestion in clarity) or
            any('never' in suggestion['original'].lower() for suggestion in clarity)
        )

    def test_end_to_end(self):
        """Test complete end-to-end functionality."""
        # Create a text that will trigger overall recommendations:
        # - Long text (>500 chars)
        # - Long sentences
        # - Repeated words
        text = "This damn service is terrible terrible terrible terrible. I hate how it always breaks and they never fix it! " + \
               "The customer service representatives are completely unhelpful when you try to explain the problems that you are experiencing with their product and they seem to have absolutely no interest in actually resolving the issues that their customers report to them which makes me wonder why they even bother having a support department in the first place since they never actually support anyone properly."

        # Complete analysis with all features
        analysis = self.full_filter.analyze_text(text, detailed=True)

        # Check all components of the analysis
        self.assertIn('censored_text', analysis)
        self.assertIn('contains_profanity', analysis)
        self.assertIn('sentiment', analysis)
        self.assertIn('enhancement_suggestions', analysis)

        # Verify profanity detection and censoring
        self.assertTrue(analysis['contains_profanity'])
        self.assertNotEqual(analysis['censored_text'], text)

        # Verify sentiment analysis
        self.assertEqual(analysis['sentiment']['classification'], 'negative')
        self.assertGreater(analysis['sentiment']['confidence'], 0.5)

        # Verify enhancement suggestions
        suggestions = analysis['enhancement_suggestions']
        self.assertGreater(len(suggestions['politeness_improvements']), 0)
        self.assertGreater(len(suggestions['clarity_improvements']), 0)
        self.assertGreater(len(suggestions['overall_recommendations']), 0)

    def test_custom_sentiment_lexicon(self):
        """Test custom sentiment lexicon functionality."""
        # Create a filter with custom sentiment lexicon
        custom_lexicon_filter = ProfanityFilter(
            enable_sentiment=True,
            sentiment_options={
                'custom_lexicon': {'superb': 4.0, 'catastrophic': -4.0},
                'preprocess_text': True
            }
        )

        # Test text with custom words
        text1 = "The performance is superb!"
        text2 = "The situation is catastrophic."

        analysis1 = custom_lexicon_filter.analyze_text(text1)
        analysis2 = custom_lexicon_filter.analyze_text(text2)

        # Verify the impact of custom lexicon
        self.assertEqual(analysis1['sentiment']['classification'], 'positive')
        self.assertEqual(analysis2['sentiment']['classification'], 'negative')

        # Check that custom words have higher impact
        self.assertGreater(
            analysis1['sentiment']['scores']['pos'],
            self.sentiment_filter.analyze_text("The performance is great!")['sentiment']['scores']['pos']
        )

    def test_case_insensitivity(self):
        """Test that profanity detection works regardless of casing."""
        base_word = "damn"
        variations = [
            "Damn",
            "DAMN",
            "DaMn",
            "dAmN"
        ]

        for variation in variations:
            self.assertTrue(
                self.basic_filter.has_profanity(variation),
                f"Failed to detect profanity in variant: {variation}"
            )

        # Test in sentence context
        for variation in variations:
            sentence = f"This {variation} test should detect profanity."
            self.assertTrue(
                self.basic_filter.has_profanity(sentence),
                f"Failed to detect profanity in sentence with variant: {variation}"
            )

if __name__ == "__main__":
    unittest.main()