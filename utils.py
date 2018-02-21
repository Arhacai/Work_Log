import os


def clear_screen():
    """Clear the screen to prepare it to show the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')
