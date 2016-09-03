"""Models Package"""

COUNCIL_ID = '591'


class AuthenticationFailureException(Exception):
    """Authentication failure (incorrect username or password)"""
    pass


class InvalidObjectException(Exception):
    """Object is not in valid state"""
    pass


class MultipleMatchException(Exception):
    """Multiple records were returned when only 1 was expected"""
    pass


class RecordNotFoundException(Exception):
    """Record not found"""
    pass
