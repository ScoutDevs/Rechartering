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

    @staticmethod
    def get_fields():
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

    def _hash_record(self):
        regex = re.compile('[0-9]+')
        numbers = regex.findall(self.ssn)
        string = "".join(numbers)
        return hashlib.sha256(string).hexdigest()

    def prepare_for_persist(self):
        self.duplicate_hash = self._hash_record()


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