import random

# Dictionary containing predefined colors
COLOR_BOOK = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (127, 255, 0),
    'red': (255, 49, 49),
    'blue': (30, 144, 255),
    'lightblue': (114, 188, 212),
    'lightgrey': (208, 208, 208),
    'grey': (32, 32, 32),
}


def get_random_color():
    """
    Returns a random color from COLOR_BOOK dictionary, excluding white.

    """
    return random.choice(list(COLOR_BOOK.values())[1:])
