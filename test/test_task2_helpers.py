import unittest
import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from task2.constants import KNOWN_PASSWORD_STARTS, NUMBERS, SPECIAL_CHARS
from task2.helpers import (
    bad_password_generator,
    pin_number,
)


class TestHelpers(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
