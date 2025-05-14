# magic_profanity/__init__.py
from .magic_profanity import ProfanityFilter
from .sentiment import SentimentAnalyzer
from .enhancement import TextEnhancer

__all__ = ["name", "__version__", "profanity", "SentimentAnalyzer", "TextEnhancer"]

name = "magic_profanity"
__version__ = "2.0.1"

profanity = ProfanityFilter()