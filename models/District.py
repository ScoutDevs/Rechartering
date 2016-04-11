""" District classes """
from . import Base


class District(Base.Object):
    """ District class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.number = ''
        self.name = ''

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_factory():
        return Factory()


class Validator(Base.Validator):
    """ District validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """ District Factory """

    @staticmethod
    def _get_uuid_prefix():
        return 'dst'

    @staticmethod
    def _get_object_class():
        return District

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists District objects """

    @staticmethod
    def _get_table_name():
        return 'Districts'
