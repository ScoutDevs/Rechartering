"""Models Package"""


class RecordNotFoundException(Exception):
    """Record not found"""
    pass


class InvalidObjectException(Exception):
    """Object is not in valid state"""
    pass


class MultipleMatchException(Exception):
    """Multiple records were returned when only 1 was expected"""
    pass
