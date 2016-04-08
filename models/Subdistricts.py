""" Subdistricts classes """
from . import Base


class Subdistricts(Base.Object):

    """ Subdistricts class """

    @staticmethod
    def get_uuid_prefix():
        return 'sbd'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):

    """ Subdistrict Validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'district_id': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'district_id': str,
            'number': str,
            'name': str,
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
