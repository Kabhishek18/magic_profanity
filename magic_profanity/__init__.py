# -*- coding: utf-8 -*-

from .magic_profanity import ProfanityFilter

__all__ = ["name", "__version__", "profanity"]

name = "magic_profanity"
__version__ = "1.0.0"

profanity = ProfanityFilter()
