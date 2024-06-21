import itertools, time, math, random

from exceptions import InvalidPasswordException
from constants import (
    MIN_ENTROPY,
    MIN_LENGTH,
    MAX_LENGTH,
    ALPHABET_LOWERCASE,
    ALPHABET_UPPERCASE,
    SPECIAL_CHARS,
    NUMBERS,
    FULL_CHAR_SET,
    KNOWN_PASSWORD_STARTS,
)


def pin_number():
    """
    Return a generator for all possible pin numbers, infinite cycle.
    This can be easily brute forced.
    """
    pin_numbers = ["".join(pin) for pin in itertools.product(NUMBERS, repeat=4)]
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


def is_valid_password(
    pwd,
    min_length=MIN_LENGTH,
    max_length=MAX_LENGTH,
    check_uppercase=False,
    check_numbers=False,
    check_special_chars=False,
    check_sub_set=False,
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
    if check_sub_set and any(sub in pwd for sub in KNOWN_PASSWORD_STARTS):
        raise InvalidPasswordException(f"Password contains one of the known subsets not in {KNOWN_PASSWORD_STARTS}")
    
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


def level_one(
    password, check_numbers=True, check_special_chars=True, check_uppercase=True, check_sub_set=True
):
    is_valid_password(
        password,
        check_numbers=check_numbers,
        check_special_chars=check_special_chars,
        check_uppercase=check_uppercase,
        check_sub_set=check_sub_set,
    )


def level_two(password):
    entropy_value = entropy_estimate(password)
    if entropy_value <= MIN_ENTROPY:
        raise InvalidPasswordException(
            f"Entropy {entropy_value} is less than the minimum {MIN_ENTROPY}"
        )


def level_three(password):
    entropy_value = compute_exact_password_entropy(password)
    if entropy_value <= MIN_ENTROPY:
        raise InvalidPasswordException(
            f"Entropy {entropy_value} is less than the minimum {MIN_ENTROPY}"
        )


def level_four(passwords):
    if len(passwords) < 100:
        raise InvalidPasswordException("Must pass at least 100 passwords to test")
    if len(passwords) != len(set(passwords)):
        raise InvalidPasswordException("Cannot include repeats in the password creation")
