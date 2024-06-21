import math
import unittest

from exceptions import InvalidPasswordException
from constants import ALPHABET_LOWERCASE, KNOWN_PASSWORD_STARTS, NUMBERS, SPECIAL_CHARS
from helpers import (
    compute_exact_password_entropy,
    compute_number_of_solutions,
    entropy,
    estimate_time_to_crack_password,
    is_valid_password,
    bad_password_generator,
    pin_number,
    entropy_estimate,
)


class TestUtils(unittest.TestCase):
    def test_pin_number(self):
        pin_number_gen = pin_number()
        for _i in range(10):
            pin = next(pin_number_gen)
            self.assertEqual(len(pin), 4)
            self.assertTrue(isinstance(pin, str))
            self.assertTrue(all(s.isnumeric() for s in pin))

    def test_bad_password_generator(self):
        bad_password_generator_gen = bad_password_generator()
        for _i in range(10):
            password = next(bad_password_generator_gen)
            self.assertTrue(password[:-2] in KNOWN_PASSWORD_STARTS)
            self.assertTrue(all(s in NUMBERS + SPECIAL_CHARS for s in password[-2]))

    def test_is_valid_password_success(self):
        # The simple case all lowercase 8 chars long
        self.assertTrue(is_valid_password("abcdefgh"))
        # Numbers required
        self.assertTrue(is_valid_password("abcdefg1", check_numbers=True))
        # Uppercase required
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
            (
                f"{KNOWN_PASSWORD_STARTS[0]}0?2",
                f"Password contains one of the known subsets not in {KNOWN_PASSWORD_STARTS}",
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

    def test_entropy_estimate(self):
        # Purely lowercase
        self.assertEqual(entropy_estimate("helloooo"), 8 * math.log2(26))
        # Lower case and upper case
        self.assertEqual(entropy_estimate("helloooA"), 8 * math.log2(52))
        # Lower case, upper case and numbers
        self.assertEqual(entropy_estimate("hell1ooA"), 8 * math.log2(62))
        # Lower case, upper case, numbers and special chars
        self.assertEqual(entropy_estimate("hell1o!A"), 8 * math.log2(67))
        # Upper case, lowercase and special chars
        self.assertEqual(entropy_estimate("PASSWO$a"), 8 * math.log2(57))
        # Numbers and lower case letters
        self.assertEqual(entropy_estimate("1234567a"), 8 * math.log2(36))
        # Numbers, lower case letters and special characters
        self.assertEqual(entropy_estimate("123456!a"), 8 * math.log2(41))
        # Lower case and special characters
        self.assertEqual(entropy_estimate("passwor!"), 8 * math.log2(31))

        # Raises error on invalid password
        with self.assertRaises(
            InvalidPasswordException, msg="Password must be at most 8 characters long"
        ):
            entropy_estimate("pwd")

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
