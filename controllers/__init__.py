"""

Controllers are read-only; they can read from the DB, but never write to it.
"""


class InvalidActionException(Exception):
    """ The action attempted is not valid """
    pass
