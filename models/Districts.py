""" Districts classes """
from . import Base


class Districts(Base.Object):

    """ Districts class """

    @staticmethod
    def get_uuid_prefix():
        return 'dst'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ Districts Factory """

    @staticmethod
    def _get_object_class():
        return Districts

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Districts objects """

    @staticmethod
    def _get_table_name():
        return 'Districts'
