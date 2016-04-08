""" User classes """
import hashlib
from . import Base


class User(Base.Object):

    """ User class """

    @staticmethod
    def hash_password(password):
        """ Hashes the password """
        hashed_password = hashlib.sha256(password).hexdigest()
        return hashed_password

    @staticmethod
    def get_uuid_prefix():
        return 'usr'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'username': Base.FIELD_REQUIRED,
            'password': Base.FIELD_REQUIRED,
            'roles': Base.FIELD_OPTIONAL,
            'positions': Base.FIELD_OPTIONAL,
            'guardians': Base.FIELD_OPTIONAL,
        }


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
