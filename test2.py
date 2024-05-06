import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from task2.helpers import test_can_crack_pin_number, test_can_crack_bad_password


if __name__ == "__main__":
    # Crack a pin number
    test_can_crack_pin_number()

    # Crack a templated password
    test_can_crack_bad_password()
