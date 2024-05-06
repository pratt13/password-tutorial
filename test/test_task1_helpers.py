import math
import unittest
import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from common.exceptions import InvalidPasswordException
from task1.constants import ALPHABET_LOWERCASE, SPECIAL_CHARS
from task1.helpers import (
    compute_exact_password_entropy,
    compute_number_of_solutions,
    entropy,
    estimate_time_to_crack_password,
    is_valid_password,
)


class TestUtils(unittest.TestCase):
    def test_is_valid_password_success(self):
        # The simple case all lowercase 8 chars long
        self.assertTrue(is_valid_password("abcdefgh"))
        # Numbers required
        self.assertTrue(is_valid_password("abcdefg1", check_numbers=True))
        # Numbers required
        self.assertTrue(is_valid_password("abcdefgH", check_uppercase=True))
        # Special characters required
        self.assertTrue(is_valid_password("abcdefg?", check_special_chars=True))
        # Min length 1
        self.assertTrue(is_valid_password("a", min_length=1))
        # Max length 10
        self.assertTrue(is_valid_password("a" * 10, max_length=10))

    def test_is_valid_password_failure_simple(self):
        for (pwd, expected_failure_message) in [
            ("aB1d??ghh", "Password must be at most 8 characters long"),
            ("aB1d??", "Password must be at least 8 characters long"),
            ("AB??HH11", "Password must contain at least one lowercase letter"),
            ("ab??hh11", "Password must contain at least one uppercase letter"),
            ("ab??hhBB", "Password must contain at least one number"),
            (
                "ab11hhBB",
                f"Password must contain at least one special character from {SPECIAL_CHARS}",
            ),
        ]:
            with self.subTest(
                "Is valid password failure",
                pwd=pwd,
                expected_failure_message=expected_failure_message,
            ):
                with self.assertRaises(InvalidPasswordException, msg=expected_failure_message):
                    is_valid_password(
                        pwd,
                        check_special_chars=True,
                        check_numbers=True,
                        check_uppercase=True,
                        min_length=8,
                        max_length=8,
                    )

    def test_entropy(self):
        self.assertEqual(entropy(5, 2), math.log2(5**2))

    def test_compute_exact_password_entropy(self):
        self.assertEqual(compute_exact_password_entropy("abB12[]"), math.log2(7**7))
        self.assertEqual(compute_exact_password_entropy("a222222"), math.log2(2**7))

    def test_compute_number_of_solution(self):
        self.assertEqual(compute_number_of_solutions(ALPHABET_LOWERCASE, 5), 26**5)

    def test_estimate_time_to_crack_password(self):
        self.assertEqual(
            estimate_time_to_crack_password(ALPHABET_LOWERCASE, 5, number_checks_per_second=10000),
            (26**5) / 10000,
        )


if __name__ == "__main__":
    unittest.main()
