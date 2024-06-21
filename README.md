# Magic Profanity

`magic_profanity` is a Python library for detecting and censoring profanity in text using customizable word lists and character mappings. It support English and Hinglish

## Installation

You can install `magic_profanity` using pip:

```python
pip install magic_profanity
```

## Requirements

- `Python 3+`

## Usage

### Importing the Library

```python
from magic_profanity import MagicProfanity
```
### Initializing the Profanity Filter

#### Create an instance of MagicProfanity:
```python
profanity_filter = MagicProfanity()
```

### Loading Custom Words
You can load custom words into the profanity filter either from a list or from a file:

### Load words from a list
```python
profanity_filter.load_censor_words(["badword1", "badword2"])
```
### Load words from a file
```python
profanity_filter.load_censor_words_from_file("path/to/custom_wordlist.txt")
```

Checking for Profanity
You can check if a text contains profanity using contains_profanity:

```python
text = "This sentence contains a badword1 and a BadWord2."
if profanity_filter.contains_profanity(text):
    print("Profanity detected!")
else:
    print("No profanity found.")
```    

### Censoring Text
You can censor profanity in text using censor:

```python 
censored_text = profanity_filter.censor(text)
print(censored_text)
```

### Adding Custom Words
You can add custom words to the profanity filter:

```python 
profanity_filter.add_censor_words(["newbadword1", "newbadword2"])
```

### Custom Character Mappings
You can customize character mappings used for censoring:

```python
profanity_filter.char_map = {
    "a": ("a", "@", "*", "4"),
    "i": ("i", "*", "l", "1"),
    "o": ("o", "*", "0", "@"),
    # Add more mappings as needed
}
```

#Contributing
Contributions are welcome! If you have any suggestions, bug reports, or enhancements, please open an issue or a pull request on GitHub.

#License
This project is licensed under the MIT License - see the LICENSE file for details.




