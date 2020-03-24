""" Formi is a Python application that can format a copied rows/cells into comma separated text. """

from collections import Counter


# [] TODO: combine this two function into 1 function, probably called 'format_text(text, separator)
def join_string(text: str, delimiter: str = ',') -> str:
    """ Return formatted text separated by a customizable delimiter, default is comma ','. """

    return text.replace('\n', f'{delimiter} ')


def expand_string(text: str) -> str:
    """ Return formatted text separated by newline '\n'. """

    return '\n'.join(text.split()).replace(',', '')


def count_input(text: str) -> int:
    """ Count total number of input text based using str.split() """

    return len(text.split(sep='\n'))


def remove_duplicate(text: str) -> list:
    """ Return list with unique elements """

    return list(Counter(text.split('\n')))
