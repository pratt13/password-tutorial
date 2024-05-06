# Task1 Help

The task is to implement

```py
def pin_number_solver():
    """
    Return a generator/list of possible solutions
    """
    raise NotImplementedError


def bad_password_solver():
    """
    Given that a password will start with a prefix : ("Qwerty", "Password", "Pa$$w0rd")
    and end in a combination of 2 characters made up of numbers or special characters
    return a list of possible solutions.
    """
    raise NotImplementedError

```

## Hint 1 - PIN
The aim is to return a list of all possible 4 digit pin numbers.
A starting point is to create a for loop(s) to do this.

## Hint 2 - PIN
The most simple solution is create a list with 4 four loop, over all possible numbers, and adding it to a list that is returned.

## Hint3 - PIN
The issue with large lists = large memory.
`itertools` is a package that has product that can return a generator that is memory efficient.

## Hint 1 - bad_password_solver
The password is comprised of a prefix that is one of three options, the rest can be brute forced.

## Hint2 - bad_password_solver
Again, `itertools` would be useful.
