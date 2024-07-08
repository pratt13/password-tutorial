"""
Task 1 script
Write your solutions for boyle's part here
"""
import itertools

NUMBERS = "0123456789"
SPECIAL_CHARS="£$?!_"
KNOWN_PASSWORD_STARTS = ("Qwerty", "Password", "Pa$$w0rd", "yoghurt", "cagney", "lacey")

def terrys_task():
    """
    Given that a password will start with a prefix : ("Qwerty", "Password", "Pa$$w0rd", "yoghurt", "cagney", "lacey")
    and end in a combination of 2 characters made up of numbers or special characters
    return a list of ALL possible solutions.
    """
    return [
        prefix + "".join(suffix)
        for suffix in itertools.product(NUMBERS + SPECIAL_CHARS, repeat=2)
        for prefix in KNOWN_PASSWORD_STARTS
    ]