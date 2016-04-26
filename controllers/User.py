# pylint: disable=import-error
"""User Controller"""
import CRUD
from models import User


class Controller(CRUD.Controller):
    """User CRUD Controller

    A 'User' is a parent or guardian of one or more youth.
    """

    def __init__(self, user, factory=None):
        if not factory:
            self.factory = User.Factory()
        super(Controller, self).__init__(user, factory)
