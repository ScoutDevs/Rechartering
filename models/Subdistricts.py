""" Subdistricts classes """
from . import Base


class Subdistricts(Base.Object):

    """ Subdistricts class """

    @staticmethod
    def get_uuid_prefix():
        return 'sbd'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'district_id': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ Subdistricts Factory """

    @staticmethod
    def _get_object_class():
        return Subdistricts

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Subdistricts objects """

    @staticmethod
    def _get_table_name():
        return 'Subdistricts'
