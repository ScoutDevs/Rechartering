# pylint: disable=import-error
"""Volunteer Controller"""
import CRUD
from models import Volunteer


class Controller(CRUD.Controller):
    """Volunteer CRUD Controller"""

    def __init__(self, user, factory=None):
        if not factory:
            self.factory = Volunteer.Factory()
        super(Controller, self).__init__(user, factory)
