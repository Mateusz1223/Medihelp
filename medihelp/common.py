from medihelp.errors import IllegalCharactersInANameError
from typing import Iterable


def set_of_strings_to_string(set_of_strings: Iterable[str]):
    result = ''
    for s in set_of_strings:
        result += s + ', '
    return result[:-2]


def normalize_name(name: str):
    name = name.strip()
    for char in ["'", '"', '\n', ',']:
        if char in name:
            raise IllegalCharactersInANameError
    return name


def normalize_list_of_names(list_of_names):
    list_of_names = [normalize_name(name) for name in list_of_names]
    while '' in list_of_names:
        list_of_names.remove('')
    return list_of_names
