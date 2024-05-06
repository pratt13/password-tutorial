import string

MIN_ENTROPY = 20
MIN_LENGTH = 8
MAX_LENGTH = 8
ALPHABET_LOWERCASE = string.ascii_lowercase
ALPHABET_UPPERCASE = string.ascii_uppercase
NUMBERS = "".join((str(n) for n in range(0, 10)))
SPECIAL_CHARS = "£$?!_"

FULL_CHAR_SET = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBERS + SPECIAL_CHARS
