# pylint: disable=import-error
"""Guardian Controller"""
import CRUD
from models import Guardian


class Controller(CRUD.Controller):
    """Guardian CRUD Controller

    A 'Guardian' is a parent or guardian of one or more youth.
    """

    def __init__(self, user, factory=None):
        if not factory:
            self.factory = Guardian.Factory()
        super(Controller, self).__init__(user, factory)
