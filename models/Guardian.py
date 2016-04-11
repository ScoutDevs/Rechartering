""" Guardian classes """
from . import Base


class Guardian(Base.Object):
    """ Guardian class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.first_name = ''
        self.last_name = ''
        self.youth = ''

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


class Factory(Base.Factory):

    """ Guardian Factory """

    @staticmethod
    def _get_object_class():
        return Guardian

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Guardian objects """

    @staticmethod
    def _get_table_name():
        return 'Guardian'
