# pylint: disable=no-member
"""Session classes"""
from datetime import datetime
from datetime import timedelta

from . import Base


class Session(Base.Object):
    """Session class"""

    EXPIRES_AFTER_SECONDS = 86400

    def __init__(self, user_uuid=None):
        super(self.__class__, self).__init__()
        self.uuid = self.get_uuid()
        self.user_uuid = user_uuid
        self.expires = datetime.now() + timedelta(seconds=self.EXPIRES_AFTER_SECONDS)
        self.data = {}

    def set(self, var, val):
        """Set a session variable"""
        self.data[var] = val

    def get(self, var):
        """Get a session variable"""
        return self.data[var]

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'ses'


class Validator(Base.Validator):
    """Session validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'expires': Base.FIELD_REQUIRED,
            'data': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """Session Factory"""

    @staticmethod
    def _get_object_class():
        return Session

    @staticmethod
    def get_persister():
        return Persister()


class Persister(Base.Persister):
    """Persists Session objects"""

    @staticmethod
    def _get_table_name():
        return 'Session'
