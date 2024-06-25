import itertools, time, math

from common.exceptions import InvalidPasswordException, TestFailureException
from task1.constants import (
    COMMON_SUB_STRINGS,
    MIN_LENGTH,
    MAX_LENGTH,
    ALPHABET_LOWERCASE,
    ALPHABET_UPPERCASE,
    SPECIAL_CHARS,
    NUMBERS,
    FULL_CHAR_SET,
    MIN_ENTROPY,
)


import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from common.utils import test_decorator


def is_valid_password(
    pwd,
    min_length=MIN_LENGTH,
    max_length=MAX_LENGTH,
    check_uppercase=False,
    check_numbers=False,
    check_special_chars=False,
    check_sub_set=False
):
    if len(pwd) < min_length:
        raise InvalidPasswordException(f"Password must be at least {min_length} characters long")
    if len(pwd) > max_length:
        raise InvalidPasswordException(f"Password must be at most {max_length} characters long")
    if not any(s in ALPHABET_LOWERCASE for s in pwd):
        raise InvalidPasswordException("Password must contain at least one lowercase letter")
    if check_uppercase and not any(s in ALPHABET_UPPERCASE for s in pwd):
        raise InvalidPasswordException("Password must contain at least one uppercase letter")
    if check_numbers and not any(s in NUMBERS for s in pwd):
        raise InvalidPasswordException("Password must contain at least one number")
    if check_special_chars and not any(s in pwd for s in SPECIAL_CHARS):
        raise InvalidPasswordException(
            f"Password must contain at least one special character from {SPECIAL_CHARS}"
        )
    if check_sub_set and any(sub_string  in pwd for sub_string in COMMON_SUB_STRINGS):

        raise InvalidPasswordException(
            f"Password must not contain any of these common phrases {COMMON_SUB_STRINGS}"
        )
    if any(s not in FULL_CHAR_SET for s in pwd):
        raise InvalidPasswordException(f"Password contains character not in {FULL_CHAR_SET}")
    return True


def entropy_estimate(pwd):
    """
    Estimate the entropy
    There are 4 character subsets in the passwords we can assume
    * lowercase
    * uppercase
    * numbers
    * special characters
    """
    # Validate password
    is_valid_password(pwd)
    length = len(pwd)
    char_length = 0
    for char_set in [
        ALPHABET_LOWERCASE,
        ALPHABET_UPPERCASE,
        NUMBERS,
        SPECIAL_CHARS,
    ]:
        if any(s in char_set for s in pwd):
            char_length += len(char_set)
    return entropy(char_length, length)


def entropy(
    char_set_length,
    length,
):
    """
    Entropy is Log2(number of characters ^ length of password)
    """
    return math.log2(char_set_length**length)


def compute_exact_password_entropy(pwd):
    """
    The exact entropy of the password, given the password
    """
    # Number of distinct characters
    length = len(pwd)
    num_distinct_chars = len(set(s for s in pwd))
    return entropy(num_distinct_chars, length)


def compute_number_of_solutions(poss_chars, pwd_length):
    """
    The possible options are computed by = n ^ l
    n : Number of possible characters
    l: length of the password
    """
    return len(poss_chars) ** pwd_length


def estimate_time_to_crack_password(poss_chars, pwd_length, number_checks_per_second=10000):
    """
    Estimate how long it is to crack a password
    Assuming n checks per second.
    """
    return compute_number_of_solutions(poss_chars, pwd_length) / number_checks_per_second


def how_long_to_crack_password(pwd, char_set=FULL_CHAR_SET, max_iter=100000000):
    start_time = time.time()
    pwd_length = len(pwd)
    guess = "a" * pwd_length
    iter_count = 0
    success = False
    poss_solutions = itertools.product(char_set, repeat=pwd_length)
    while iter_count < max_iter and not success:
        values = next(poss_solutions)
        guess = "".join(values)
        if guess == pwd:
            success = True
            break
        iter_count += 1
    end_time = time.time()
    if success:
        print(f"Time to guess password = {end_time-start_time}")
    else:
        print(f"Failed to get password after {end_time-start_time}")
        if iter_count >= max_iter:
            print(f"Max iteration of {max_iter} exceeded")


## Tests


@test_decorator("Is valid Password", 1, iter=1000)
def test_is_valid_password(pwd_generator):
    """
    Test to check the password generator is valid
    If it raises a value error then except it as it is
    an expected error but rethrow.
    """
    res = False
    pwd = pwd_generator()
    try:
        res = is_valid_password(pwd)
    except InvalidPasswordException as e:
        raise TestFailureException(e.message)
    return res


@test_decorator("Exceeds entropy estimate", 2, iter=1000)
def test_entropy_estimate(pwd_generator):
    pwd = pwd_generator()
    if entropy_estimate(pwd) > MIN_ENTROPY:
        return True
    else:
        raise TestFailureException(
            f"Entropy {entropy_estimate(pwd)} is less than the minimum {MIN_ENTROPY}"
        )


@test_decorator("Exceeds actual entropy", 3, iter=1000)
def test_exact_entropy(pwd_generator):
    pwd = pwd_generator()
    if compute_exact_password_entropy(pwd) > MIN_ENTROPY:
        return True
    else:
        raise TestFailureException(
            f"Entropy {compute_exact_password_entropy(pwd)} is less than the minimum {MIN_ENTROPY}"
        )


@test_decorator("No Repeats", 4, iter=1000)
def test_no_repeats(pwd_generator):
    num_tries = 10
    passwords = [pwd_generator() for i in range(num_tries)]
    if len(passwords) == num_tries:
        return True
    else:
        raise TestFailureException(f"Repeat passwords generated in {num_tries} tries")


@test_decorator("No repeat pattern", 5, iter=1000)
def test_char_distribution(pwd_generator):
    """
    We should check distribution, but this is simple.
    Every type of char in the repeats must appear in a position
    """
    num_tries = 100
    passwords = [pwd_generator() for i in range(num_tries)]
    resorted_passwords = [
        "".join([passwords[i][j] for i in range(num_tries)]) for j in range(len(passwords[0]))
    ]
    print(resorted_passwords)
    result = False
    try:
        if all(
            is_valid_password(pwd, max_length=num_tries, min_length=num_tries)
            for pwd in resorted_passwords
        ):
            result = True
    except ValueError:
        raise TestFailureException(
            f"Some characters never appear in a particular position after {num_tries} tries"
        )
    return result
