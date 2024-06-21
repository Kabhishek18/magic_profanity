from io import open
from json import load
from string import ascii_letters, digits

from .utils import get_complete_path_of_file

ALLOWED_CHARACTERS = set(ascii_letters) | set(digits) | {"@", "#", "%", "&", "$", "*", '"', "'"}
file_path = get_complete_path_of_file("unicode.json")

try:
    with open(file_path, "r", encoding="utf-8") as json_file:
        additional_characters = load(json_file)
        if isinstance(additional_characters, (list, set)):
            ALLOWED_CHARACTERS.update(additional_characters)
        else:
            print(f"Warning: Invalid format in unicode.json - expected list or set, got {type(additional_characters)}")
except FileNotFoundError as e:
    print(f"Error: File '{file_path}' not found - {e}")
except IOError as e:
    print(f"Error: IOError occurred while opening '{file_path}' - {e}")
except ValueError as e:
    print(f"Error: JSON parsing error in '{file_path}' - {e}")
