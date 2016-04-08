""" Youth classes """
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
        }


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
