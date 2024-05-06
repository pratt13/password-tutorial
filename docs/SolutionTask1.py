import random

from common.constants import ALPHABET_LOWERCASE, ALPHABET_UPPERCASE, NUMBERS, SPECIAL_CHARS


def generate_password():
    """
    A Function to implement to generate a password
    Must be 8 character longs
    Contain:
     * lowercase letter
     * uppercase letter
     * number
     * one of £$%&:@;_-+=[]{}?
    """
    chars = (
        random.sample(SPECIAL_CHARS, 2)
        + random.sample(NUMBERS, 2)
        + random.sample(ALPHABET_UPPERCASE, 2)
        + random.sample(ALPHABET_LOWERCASE, 2)
    )
    random.shuffle(chars)
    return "".join(chars)
