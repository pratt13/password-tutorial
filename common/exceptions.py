class TestFailureException(Exception):
    """Exception raised for when a test fails."""

    pass


class InvalidPasswordException(Exception):
    """Exception raised for when a password is invalid"""

    pass



class InvalidUserForPage(Exception):
    """Exception raised for when a username for that page is invalid"""

    pass
