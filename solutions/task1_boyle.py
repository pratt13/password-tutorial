"""
Task 1 script
Write your solutions for boyle's part here
"""
import itertools

NUMBERS = "0123456789"


def boyles_task():
    """
    Return a generator/list of ALL possible solutions for a pin number 4 digits long
    """
    return ["".join(pin) for pin in itertools.product(NUMBERS, repeat=4)]