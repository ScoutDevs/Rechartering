# pylint: disable=no-member
""" Volunteers classes """
import hashlib
import re
from . import Base


class Volunteers(Base.Object):  # pylint: disable=too-many-instance-attributes
    """ Volunteers class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.duplicate_hash = ''
        self.unit_id = ''
        self.scoutnet_id = ''
        self.application_id = ''
        self.ypt_completion_date = ''
        self.first_name = ''
        self.last_name = ''
        self.ssn = ''

    @staticmethod
    def get_uuid_prefix():
        return 'vol'

    def get_validator(self):
        return Validator(self)

    def get_record_hash(self):
        """ Compile record hash to allow for easy duplicate checks """
        regex = re.compile('[0-9]+')
        numbers = regex.findall(self.ssn)
        string = "".join(numbers)
        return hashlib.sha256(string).hexdigest()

    def prepare_for_validate(self):
        self.duplicate_hash = self.get_record_hash()


class Validator(Base.Validator):
    """ Volunteer validator """

    @staticmethod
    def get_field_requirements():
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

    """ Volunteers Factory """

    @staticmethod
    def _get_object_class():
        return Volunteers

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Volunteers objects """

    @staticmethod
    def _get_table_name():
        return 'Volunteers'
