""" Units classes """
from . import Base


class Units(Base.Object):

    """ Units class """

    @staticmethod
    def get_uuid_prefix():
        return 'unt'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'sponsoring_organization_id': Base.FIELD_REQUIRED,
            'type': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ Units Factory """

    @staticmethod
    def _get_object_class():
        return Units

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Units objects """

    @staticmethod
    def _get_table_name():
        return 'Units'
