# Task1 Help

The task is to implement

```py
def generate_password():
    """
    A Function to implement to generate a password
    Must be 8 character longs
    Contain:
     * lowercase letter
     * uppercase letter
     * number
     * one of `£$?!_`
    """
    raise NotImplementedError
```

## Hint 1
So the first step is to replace `raise NotImplementedError` with something that satisfies all the four conditions.
This can be just an 8 character password that you think of now that passes those criteria.
Then run the test script.

This will likely fail to more stricter conditions that passwords would meet.

## Hint 2
Randomness is an important part to passwords, so is usually the case in python, lets import a library that helps to do this.
Python `random` library is excellent for our task.


## Hint3
The key is if you were to run this
```
generate_password()
generate_password()
generate_password()
```
would we:
* see the same password?
* see the same structure in the password. For example, `1234ab?C` and `8721ds!G` are different, the sequence of the characters are the same, implying the algorithm is not truly random. (Although a truly random password could produce results that seem unlikely).
