# pylint: disable=no-member
"""Volunteer classes"""
import hashlib
import re

from . import Base


class Volunteer(Base.Object):  # pylint: disable=too-many-instance-attributes
    """Volunteer class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.user_uuid = ''
        self.duplicate_hash = ''
        self.unit_id = ''
        self.scoutnet_id = ''
        self.application_id = ''
        self.ypt_completion_date = ''
        self.first_name = ''
        self.last_name = ''
        self.ssn = ''

    def get_validator(self):
        return Validator(self)

    def get_record_hash(self):
        """Compile record hash to allow for easy duplicate checks"""
        regex = re.compile('[0-9]+')
        numbers = regex.findall(self.ssn)
        string = "".join(numbers)
        return hashlib.sha256(string).hexdigest()

    @staticmethod
    def get_factory():
        return Factory()


class Validator(Base.Validator):
    """Volunteer validator"""

    def prepare_for_validate(self):
        self.obj.duplicate_hash = self.obj.get_record_hash()

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'duplicate_hash': Base.FIELD_REQUIRED,
            'unit_id': Base.FIELD_REQUIRED,
            'scoutnet_id': Base.FIELD_OPTIONAL,
            'application_id': Base.FIELD_OPTIONAL,
            'ypt_completion_date': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'ssn': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """Volunteer Factory"""

    @staticmethod
    def get_uuid_prefix():
        return 'vol'

    @staticmethod
    def _get_object_class():
        return Volunteer

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """Persists Volunteer objects"""

    @staticmethod
    def _get_table_name():
        return 'People'
