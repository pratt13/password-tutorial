import string

MIN_ENTROPY = 16  # Password of 8 characters and 4 repeats 8(log_2(4))
MIN_LENGTH = 8
MAX_LENGTH = 8
ALPHABET_LOWERCASE = string.ascii_lowercase
ALPHABET_UPPERCASE = string.ascii_uppercase
NUMBERS = "".join((str(n) for n in range(0, 10)))
SPECIAL_CHARS = "£$?!_"

FULL_CHAR_SET = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE + NUMBERS + SPECIAL_CHARS
KNOWN_PASSWORD_STARTS = ("Qwerty", "Password", "Pa$$w0rd", "yoghurt", "cagney", "lacey")
