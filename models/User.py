"""User classes"""
import hashlib

from . import Base


class User(Base.Object):  # pylint: disable=too-many-instance-attributes
    """User class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.uuid = self.get_uuid()
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.password = ''
        self.guardian_id = ''
        self.roles = {}
        self.positions = []

    @staticmethod
    def hash_password(password):
        """Hashes the password"""
        hashed_password = hashlib.sha256(password).hexdigest()
        return hashed_password

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'usr'


class Validator(Base.Validator):
    """User validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'username': Base.FIELD_REQUIRED,
            'password': Base.FIELD_REQUIRED,
            'roles': Base.FIELD_OPTIONAL,
            'positions': Base.FIELD_OPTIONAL,
            'guardians': Base.FIELD_OPTIONAL,
        }
# TO-DO: UUID = usr-[USERNAME]


class Factory(Base.Factory):
    """User Factory"""

    @staticmethod
    def load_by_session(session_id):
        """Load the user based on the session UUID"""
        # TO-DO: implement this
        return session_id

    @staticmethod
    def _get_object_class():
        return User

    @staticmethod
    def get_persister():
        return Persister()


class Persister(Base.Persister):

    """Persists User objects"""

    @staticmethod
    def _get_table_name():
        return 'Users'
