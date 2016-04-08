""" Guardians classes """
from . import Base


class Guardians(Base.Object):

    """ Guardians class """

    @staticmethod
    def get_uuid_prefix():
        return 'gdn'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'youth': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ Guardians Factory """

    @staticmethod
    def _get_object_class():
        return Guardians

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Guardians objects """

    @staticmethod
    def _get_table_name():
        return 'Guardians'
