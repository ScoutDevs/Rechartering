# pylint: disable=import-error
"""User Controller"""
from models import User

from . import CRUD


class Controller(CRUD.Controller):
    """User Controller

    A 'User' is anyone with an account.
    """

    def __init__(self, user, factory=None):
        self.user = user
        if not factory:
            self.factory = User.Factory()
        super(Controller, self).__init__(user, factory)

    def log_in(self, username, password):
        """Attempt to authenticate and log the user in"""
        user = self.factory.load_by_username_password(username, password)
        self.user = user
        return user
