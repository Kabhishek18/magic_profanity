import os.path

def get_complete_path_of_file(filename):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)

def read_wordlist(filename):
    with open(filename, encoding="utf-8") as wordlist_file:
        for row in wordlist_file:
            row = row.strip()
            if row:
                yield row

def get_replacement_for_swear_word(censor_char):
    return censor_char * 4

def any_next_words_form_swear_word(current_word, word_indices, censor_words):
    full_word = current_word.lower()
    full_word_with_separators = current_word.lower()

    for index in range(0, len(word_indices), 2):
        single_word, end_index = word_indices[index]
        word_with_separators, _ = word_indices[index + 1]
        if single_word == "":
            continue

        full_word += single_word.lower()
        full_word_with_separators += word_with_separators.lower()
        if full_word in censor_words or full_word_with_separators in censor_words:
            return True, end_index
    return False, -1
