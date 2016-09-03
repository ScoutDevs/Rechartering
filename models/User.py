"""User classes"""
import hashlib

from . import AuthenticationFailureException
from . import Base
from . import MultipleMatchException


class User(Base.Object):  # pylint: disable=too-many-instance-attributes
    """User class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.uuid = self.get_uuid()
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.password = ''
        self.guardian_uuid = ''
        self.roles = {}
        self.positions = []

    @staticmethod
    def get_password_hash(password):
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

    def load_by_session(self, session_uuid):
        """Load the user based on the session UUID"""
        search = {
            '__index__': 'session_uuid',
            'session_uuid': session_uuid,
        }
        data = self.get_persister().query(search)
        if len(data) == 1:
            user = self.construct(data[0])
            return user
        elif len(data) > 1:  # This should never happen.
            raise MultipleMatchException('System Error 5001.')
        else:
            raise AuthenticationFailureException('Authentication failure.')

    def load_by_username_password(self, username, password):
        """Load the user based on the username & password"""
        search = {
            '__index__': 'username',
            'username': username,
            'password': User.get_password_hash(password),
        }
        data = self.get_persister().query(search)
        if len(data) == 1:
            user = self.construct(data[0])
            return user
        elif len(data) > 1:  # This should never happen.
            raise MultipleMatchException('System Error 5002.')
        else:
            raise AuthenticationFailureException('User not found.')

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
