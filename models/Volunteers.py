""" Volunteers classes """
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
            'data': Base.FIELD_REQUIRED,
            'scoutnet_id': Base.FIELD_OPTIONAL,
            'application_id': Base.FIELD_OPTIONAL,
            'YPT_completion_date': Base.FIELD_REQUIRED,
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
