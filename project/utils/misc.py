import os

def to_lowercase(input_string) -> str:
    """
    Converts a string to all lowercase.
    """
    return input_string.lower()

def get_current_path():
    """
    Returns the current working directory.
    """
    return os.getcwd()

