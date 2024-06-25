def pin_number_solver():
    """
    Return a generator/list of possible solutions
    """
    import itertools
    NUMBERS = "".join((str(n) for n in range(0, 10)))
    return ["".join(pin) for pin in itertools.product(NUMBERS, repeat=3)]


def bad_password_solver():
    """
    Given that a password will start with a prefix : ("Qwerty", "Password", "Pa$$w0rd")
    and end in a combination of 2 characters made up of numbers or special characters
    return a list of possible solutions.
    """
    raise NotImplementedError
