import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from task1.helpers import (
    test_char_distribution,
    test_entropy_estimate,
    test_exact_entropy,
    test_is_valid_password,
    test_no_repeats,
)
from task1.task1 import generate_password

if __name__ == "__main__":

    # Test is a valid password
    test_is_valid_password(generate_password)

    # Test exceeds minimum entropy
    test_entropy_estimate(generate_password)

    # Test exact entropy is big enough
    test_exact_entropy(generate_password)

    # Test no repeats
    test_no_repeats(generate_password)

    # Test that not a consistent pattern
    test_char_distribution(generate_password)
