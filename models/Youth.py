# pylint: disable=no-member,attribute-defined-outside-init
""" Youth classes """
import hashlib
import re
from . import Base


class Youth(Base.Object):

    """ Youth class """

    @staticmethod
    def get_uuid_prefix():
        return 'yth'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'duplicate_hash': Base.FIELD_REQUIRED,
            'units': Base.FIELD_REQUIRED,
            'scoutnet_id': Base.FIELD_OPTIONAL,
            'application_id': Base.FIELD_OPTIONAL,
            'guardians': Base.FIELD_OPTIONAL,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'date_of_birth': Base.FIELD_REQUIRED,
        }

    def _hash_record(self):
        regex = re.compile('[a-zA-Z0-9]+')
        match = regex.findall(self.first_name+self.last_name+self.date_of_birth)
        string = "".join(match)
        return hashlib.sha256(string).hexdigest()

    def prepare_for_persist(self):
        self.duplicate_hash = self._hash_record()


class Factory(Base.Factory):

    """ Youth Factory """

    @staticmethod
    def _get_object_class():
        return Youth

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Youth objects """

    @staticmethod
    def _get_table_name():
        return 'Youth'