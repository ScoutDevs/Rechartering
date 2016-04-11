"""
Here be controllers

Controllers should support dependency injection and should be able to be tested
completely free of DB & network dependencies.
"""


class InvalidActionException(Exception):
    """ The action attempted is not valid """
    pass
