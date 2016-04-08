# pylint: disable=no-member,attribute-defined-outside-init
""" Volunteers classes """
import hashlib
import re
from . import Base


class Volunteers(Base.Object):

    """ Volunteers class """

    @staticmethod
    def get_uuid_prefix():
        return 'vol'

    def get_validator(self):
        return Validator(self)

    def _hash_record(self):
        regex = re.compile('[0-9]+')
        numbers = regex.findall(self.ssn)
        string = "".join(numbers)
        return hashlib.sha256(string).hexdigest()

    def prepare_for_persist(self):
        self.duplicate_hash = self._hash_record()


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
            'YPT_completion_date': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'ssn': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'duplicate_hash': str,
            'unit_id': str,
            'scoutnet_id': int,
            'application_id': str,
            'YPT_completion_date': str,
            'first_name': str,
            'last_name': str,
            'ssn': str,
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
