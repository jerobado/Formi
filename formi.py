""" Formi is a Python application that can format a copied rows/cells into comma separated text. """


def join_string(text):
    """ Return formatted text separated by comma. """
    
    return text.replace('\n', ', ')
