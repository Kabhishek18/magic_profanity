# magic_profanity/sentiment.py
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re


class SentimentAnalyzer:
    def __init__(self, custom_threshold=None, custom_lexicon=None, preprocess_text=True):
        """
        Initialize the sentiment analyzer.

        Args:
            custom_threshold (dict, optional): Custom thresholds for sentiment classification
                                              e.g., {'positive': 0.1, 'negative': -0.1}
            custom_lexicon (dict, optional): Custom sentiment lexicon to augment the built-in one
                                            e.g., {'awesome': 2.0, 'terrible': -2.0}
            preprocess_text (bool): Whether to preprocess text before analysis
        """
        # Download necessary resources on first use
        try:
            nltk.data.find('vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        self.analyzer = SentimentIntensityAnalyzer()
        self.preprocess_text = preprocess_text

        # Set custom thresholds or use defaults
        self.thresholds = {
            'positive': 0.05,
            'negative': -0.05
        }
        if custom_threshold:
            self.thresholds.update(custom_threshold)

        # Add custom lexicon words if provided
        if custom_lexicon:
            self.analyzer.lexicon.update(custom_lexicon)

    def preprocess(self, text):
        """
        Preprocess text for better sentiment analysis.

        Args:
            text (str): Input text

        Returns:
            str: Preprocessed text
        """
        if not self.preprocess_text:
            return text

        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)

        # Remove excess whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Handle repeated characters (e.g., "gooooood" -> "good")
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)

        return text

    def analyze(self, text):
        """
        Analyze the sentiment of the given text.

        Args:
            text (str): The text to analyze

        Returns:
            dict: A dictionary containing sentiment scores:
                  - 'compound': Overall sentiment (-1 to 1)
                  - 'pos': Positive score (0 to 1)
                  - 'neu': Neutral score (0 to 1)
                  - 'neg': Negative score (0 to 1)
        """
        text = self.preprocess(text)
        return self.analyzer.polarity_scores(text)

    def get_sentiment(self, text):
        """
        Get a simple sentiment classification based on the compound score.

        Args:
            text (str): The text to analyze

        Returns:
            str: One of 'positive', 'neutral', or 'negative'
        """
        scores = self.analyze(text)
        compound = scores['compound']

        if compound >= self.thresholds['positive']:
            return 'positive'
        elif compound <= self.thresholds['negative']:
            return 'negative'
        else:
            return 'neutral'

    def get_detailed_analysis(self, text):
        """
        Get a detailed sentiment analysis with confidence levels.

        Args:
            text (str): The text to analyze

        Returns:
            dict: Detailed sentiment analysis including:
                  - 'classification': Main sentiment classification
                  - 'confidence': Confidence level (0-1)
                  - 'scores': Raw sentiment scores
                  - 'emotion_indicators': Detected emotion indicators
        """
        scores = self.analyze(text)
        compound = scores['compound']

        # Determine classification
        if compound >= self.thresholds['positive']:
            classification = 'positive'
            confidence = min(1.0, (compound - self.thresholds['positive']) / (1 - self.thresholds['positive']))
        elif compound <= self.thresholds['negative']:
            classification = 'negative'
            confidence = min(1.0, (self.thresholds['negative'] - compound) / (1 + self.thresholds['negative']))
        else:
            classification = 'neutral'
            # Calculate confidence based on distance from thresholds
            pos_distance = abs(compound - self.thresholds['positive'])
            neg_distance = abs(compound - self.thresholds['negative'])
            min_distance = min(pos_distance, neg_distance)
            # Convert to a confidence level (closer to a threshold = lower confidence)
            confidence = min(1.0, min_distance / (self.thresholds['positive'] - self.thresholds['negative']))

        # Detect emotion indicators from text
        emotion_indicators = self._detect_emotion_indicators(text)

        return {
            'classification': classification,
            'confidence': round(confidence, 2),
            'scores': scores,
            'emotion_indicators': emotion_indicators
        }

    def _detect_emotion_indicators(self, text):
        """
        Detect emotional indicators in text.

        Args:
            text (str): Input text

        Returns:
            dict: Detected emotions with confidence scores
        """
        # Simple emotion detection dictionary
        emotion_patterns = {
            'joy': [r'\b(happy|joy|delighted|excited|love|wonderful|great)\b', r'😊|😄|😃|😁|😀'],
            'anger': [r'\b(angry|mad|furious|outraged|annoyed)\b', r'😠|😡|🤬'],
            'sadness': [r'\b(sad|unhappy|depressed|miserable|upset)\b', r'😢|😭|😔|☹️'],
            'fear': [r'\b(afraid|scared|terrified|worried|anxious)\b', r'😨|😰|😱'],
            'surprise': [r'\b(surprised|shocked|amazed|astonished)\b', r'😲|😮|😯'],
            'disgust': [r'\b(disgusted|gross|yuck|ew)\b', r'🤢|🤮']
        }

        results = {}

        for emotion, patterns in emotion_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                score += len(matches) * 0.2  # 0.2 confidence per match

            if score > 0:
                results[emotion] = min(1.0, score)  # Cap at 1.0

        return results