from collections.abc import Iterable
from .constants import ALLOWED_CHARACTERS
from .utils import (
    any_next_words_form_swear_word,
    get_complete_path_of_file,
    get_replacement_for_swear_word,
    read_wordlist,
)
from .variant import VariantString

class ProfanityFilter:
    def __init__(self, words=None):
        if words is not None and not isinstance(words, (str, Iterable)):
            raise TypeError("Words must be of type str, Iterable, or None")
        
        self.censor_wordset = []
        self.char_map = {
            "a": ("a", "@", "*", "4"),
            "b": ("b", "8"),
            "c": ("c", "(", "[", "<"),
            "d": ("d", "6"),
            "e": ("e", "*", "3"),
            "f": ("f", "ph"),
            "g": ("g", "9", "6"),
            "h": ("h", "#"),
            "i": ("i", "*", "l", "1"),
            "j": ("j", "_|"),
            "k": ("k", "|<"),
            "l": ("l", "1", "|"),
            "m": ("m", "nn", "|\\/|"),
            "n": ("n", "|\\|"),
            "o": ("o", "*", "0", "@"),
            "p": ("p", "9"),
            "q": ("q", "9"),
            "r": ("r", "Я", "2"),
            "s": ("s", "$", "5"),
            "t": ("t", "7", "+"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "w": ("w", "vv", "\\V/"),
            "x": ("x", "%", "*", "><"),
            "y": ("y", "j"),
            "z": ("z", "2"),
        }
        self.max_num_combinations = 1
        self.allowed_characters = ALLOWED_CHARACTERS
        self.default_wordlist_filename = get_complete_path_of_file("wordlist.txt")
        
        if isinstance(words, str):
            self.load_words_from_file(words)
        else:
            self.load_words(words)

    def censor_text(self, text, censor_char="*"):
        if not self.censor_wordset:
            self.load_words()
        return self._replace_swear_words(text, censor_char)

    def load_words_from_file(self, filename, **kwargs):
        words = list(read_wordlist(filename))
        self._add_words_to_wordset(words, **kwargs)

    def load_words(self, custom_words=None, **kwargs):
        custom_words = list(custom_words) if custom_words else list(read_wordlist(self.default_wordlist_filename))
        self._add_words_to_wordset(custom_words, **kwargs)

    def add_custom_words(self, custom_words):
        if not isinstance(custom_words, (list, tuple, set)):
            raise TypeError("Function 'add_custom_words' only accepts list, tuple, or set.")
        for word in custom_words:
            self.censor_wordset.append(VariantString(word, char_map=self.char_map))

    def has_profanity(self, text):
        return text != self.censor_text(text)

    def _add_words_to_wordset(self, words, whitelist_words=None):
        if whitelist_words is not None and not isinstance(whitelist_words, (list, set, tuple)):
            raise TypeError("The 'whitelist_words' keyword argument only accepts list, tuple, or set.")
        
        whitelist_words = set(word.lower() for word in (whitelist_words or []))
        all_censor_words = []

        for word in set(words):
            word = word.lower()
            if word in whitelist_words:
                continue

            num_of_non_allowed_chars = self._count_non_allowed_characters(word)
            if num_of_non_allowed_chars > self.max_num_combinations:
                self.max_num_combinations = num_of_non_allowed_chars

            all_censor_words.append(VariantString(word, char_map=self.char_map))

        self.censor_wordset = all_censor_words

    def _count_non_allowed_characters(self, word):
        return sum(1 for char in word if char not in self.allowed_characters)

    def _update_next_word_indices(self, text, word_indices, start_idx):
        if not word_indices:
            return self._get_upcoming_words(text, start_idx, self.max_num_combinations)
        else:
            word_indices = word_indices[2:]
            if word_indices and word_indices[-1][0] != "":
                word_indices += self._get_upcoming_words(text, word_indices[-1][1], 1)
        return word_indices

    def _replace_swear_words(self, text, censor_char):
        censored_text = []
        cur_word = []
        skip_index = -1
        next_word_indices = []
        start_idx = self._find_start_index_of_next_word(text, 0)

        if start_idx >= len(text) - 1:
            return text

        censored_text.append(text[:start_idx])
        text = text[start_idx:]

        for index, char in enumerate(text):
            if index < skip_index:
                continue
            if char in self.allowed_characters:
                cur_word.append(char)
                continue

            if not cur_word:
                censored_text.append(char)
                continue

            next_word_indices = self._update_next_word_indices(text, next_word_indices, index)
            contains_swear_word, end_index = any_next_words_form_swear_word(
                "".join(cur_word), next_word_indices, self.censor_wordset
            )
            if contains_swear_word:
                cur_word = [get_replacement_for_swear_word(censor_char)]
                skip_index = end_index
                next_word_indices = []

            if "".join(cur_word).lower() in self.censor_wordset:
                cur_word = [get_replacement_for_swear_word(censor_char)]

            censored_text.extend(cur_word)
            censored_text.append(char)
            cur_word = []

        if cur_word and skip_index < len(text) - 1:
            if "".join(cur_word).lower() in self.censor_wordset:
                cur_word = [get_replacement_for_swear_word(censor_char)]
            censored_text.extend(cur_word)
        
        return "".join(censored_text)

    def _find_start_index_of_next_word(self, text, start_idx):
        for index in range(start_idx, len(text)):
            if text[index] in self.allowed_characters:
                return index
        return len(text)

    def _get_next_word_and_end_index(self, text, start_idx):
        next_word = []
        for index in range(start_idx, len(text)):
            if text[index] in self.allowed_characters:
                next_word.append(text[index])
            else:
                break
        return "".join(next_word), index

    def _get_upcoming_words(self, text, start_idx, num_of_next_words=1):
        start_idx_of_next_word = self._find_start_index_of_next_word(text, start_idx)
        if start_idx_of_next_word >= len(text) - 1:
            return [("", start_idx_of_next_word), ("", start_idx_of_next_word)]

        next_word, end_index = self._get_next_word_and_end_index(text, start_idx_of_next_word)
        words = [(next_word, end_index), (text[start_idx:start_idx_of_next_word] + next_word, end_index)]

        if num_of_next_words > 1:
            words.extend(self._get_upcoming_words(text, end_index, num_of_next_words - 1))

        return words
