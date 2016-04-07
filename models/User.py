""" User classes """
from . import Base


class User(Base.Object):

    """ User class """

    @staticmethod
    def get_uuid_prefix():
        return 'usr'

    @staticmethod
    def get_fields():
        return [
            'uuid',
            'username',
            'password',
            'roles',
            'positions',
            'guardians'
        ]

    def valid(self):
        return True


class Factory(Base.Factory):

    """ User Factory """

    @staticmethod
    def _get_object_class():
        return User

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists User objects """

    @staticmethod
    def _get_table_name():
        return 'Users'
