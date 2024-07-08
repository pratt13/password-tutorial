import random
import string

ALPHABET_LOWERCASE = string.ascii_lowercase
ALPHABET_UPPERCASE = string.ascii_uppercase
NUMBERS = "0123456789"
SPECIAL_CHARS="£$?!_"
KNOWN_PASSWORD_STARTS = ("Qwerty", "Password", "Pa$$w0rd", "yoghurt", "cagney", "lacey")


def generate_password():
    """
    Task2
    A Function to implement to generate a password
    Must be 8 character longs
    Contain:
     * lowercase letter
     * uppercase letter
     * number
     * one of £$?!_
     * No examples of `Qwerty, Password, Pa$$w0rd, yoghurt, cagney, lacey`
     * No repeats within 100 tries
     * Range of characters, not all the letter `a1a2a3a4`
     * All characters are randomly and uniformly chosen.

    It should also not be predictable in any way.
    """
    chars = (
        random.sample(SPECIAL_CHARS, 2)
        + random.sample(NUMBERS, 2)
        + random.sample(ALPHABET_UPPERCASE, 2)
        + random.sample(ALPHABET_LOWERCASE, 2)
    )
    random.shuffle(chars)
    return "".join(chars)