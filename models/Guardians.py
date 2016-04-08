""" Guardians classes """
from . import Base


class Guardians(Base.Object):

    """ Guardians class """

    @staticmethod
    def get_uuid_prefix():
        return 'gdn'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ Guardian validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'youth': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'first_name': str,
            'last_name': str,
            'youth': list,
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
