"""Models Package"""


class RecordNotFoundException(Exception):
    """Record not found"""
    pass


class InvalidObjectException(Exception):
    """Object is not in valid state"""
    pass
