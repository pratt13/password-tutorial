import random
import itertools

# from task2 import pin_number_solver, bad_password_solver

import sys
import os

from task2.task2 import bad_password_solver, pin_number_solver

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from common.utils import test_decorator
from task2.constants import KNOWN_PASSWORD_STARTS, NUMBERS, SPECIAL_CHARS


def pin_number():
    """
    Return a generator for all possible pin numbers, infinite cycle.
    This can be easily brute forced.
    """
    pin_numbers = ["".join(pin) for pin in itertools.product(NUMBERS, repeat=3)]
    random.shuffle(pin_numbers)
    return itertools.cycle(pin_numbers)


def bad_password_generator():
    """
    Generate a bad password with given prefixes KNOWN_PASSWORD_STARTS
    and endings being combination of numbers and special characters as the last 4
    elements in the password.
    Returns a generator of the set of passwords.
    """
    possible_password_templates = KNOWN_PASSWORD_STARTS
    passwords = [
        password_prefix + "".join(password_ending)
        for password_prefix in possible_password_templates
        for password_ending in itertools.product(NUMBERS + SPECIAL_CHARS, repeat=2)
    ]
    random.shuffle(passwords)
    return itertools.cycle(passwords)


def crack_the_password(password_generator, password_cracker, max_iter=10000, verbose=False):
    """
    Given a password generator, and a cracker, can the cracker solver the generator after
    n iterations. Max_iter determines the number of iterations.
    On success, return True, else False.
    """
    password_to_guess = next(password_generator())
    num_iterations = 0
    success = False
    password_solver = (password for password in password_cracker())
    while num_iterations < max_iter:
        if next(password_solver) == password_to_guess:
            success = True
            if verbose:
                print(f"Successfully cracked it, it was {password_to_guess}")
            break
        num_iterations += 1
    if not success:
        print(f"Failed to find password after {max_iter} iterations")
    return success


## Tests to run
@test_decorator("Can crack a pin number", 1, iter=1000)
def test_can_crack_pin_number():
    return crack_the_password(pin_number, pin_number_solver)


@test_decorator("Can crack a bad password", 2, iter=1000)
def test_can_crack_bad_password():
    return crack_the_password(bad_password_generator, bad_password_solver, max_iter=1000000)
