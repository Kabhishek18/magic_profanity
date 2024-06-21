from typing import Dict, Iterator, Tuple

class VariantString:
    def __init__(self, string, char_map=None):
        if char_map is None:
            char_map = {}
        self._original = string
        self._char_map = char_map
        self._min_len = 0
        self._max_len = 0
        self._char_combos = []
        for char in self._original:
            if char in self._char_map:
                substitutions = self._char_map[char]
                self._char_combos.append(substitutions)
                lengths = [len(c) for c in substitutions]
                self._min_len += min(lengths)
                self._max_len += max(lengths)
            else:
                self._char_combos.append((char,))
                self._min_len += 1
                self._max_len += 1

    def __str__(self):
        return self._original

    def __repr__(self):
        return f"VariantString({self._original!r}, {self._char_map!r})"

    def __eq__(self, other):
        if isinstance(other, VariantString):
            raise NotImplementedError("Comparison between VariantString instances is not supported.")
        elif isinstance(other, str):
            if len(other) < self._min_len or len(other) > self._max_len:
                return False
            return self._match_variants(other)
        return False

    def _match_variants(self, other):
        slices = [other]
        for chars in self._char_combos:
            new_slices = []
            for slice in slices:
                for char in chars:
                    if slice.startswith(char):
                        new_slices.append(slice[len(char):])
            slices = new_slices
        return "" in slices

    def __hash__(self):
        return hash(self._original)

    def __len__(self):
        return len(self._original)

    def variants(self):
        return self._variant_iter()

    def _variant_iter(self):
        if self._char_combos:
            yield from self._iter_variants(0, "")
        else:
            yield self._original

    def _iter_variants(self, idx, current):
        if idx == len(self._char_combos):
            yield current
        else:
            for char in self._char_combos[idx]:
                yield from self._iter_variants(idx + 1, current + char)
