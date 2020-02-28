""" Formi is a Python application that can format a copied rows/cells into comma separated text. """


# [] TODO: combine this two function into 1 function, probably called 'format_text(text, separator)
def join_string(text: str) -> str:
    """ Return formatted text separated by comma ','. """

    return text.replace('\n', ', ')


def expand_string(text: str) -> str:
    """ Return formatted text separated by newline '\n'. """

    return '\n'.join(text.split()).replace(',', '')
