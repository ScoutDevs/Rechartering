""" Districts classes """
from . import Base


class Districts(Base.Object):

    """ Districts class """

    @staticmethod
    def get_uuid_prefix():
        return 'dst'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ Districts validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'number': str,
            'name': str,
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
