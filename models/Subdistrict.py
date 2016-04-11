""" Subdistrict classes """
from . import Base


class Subdistrict(Base.Object):
    """ Subdistrict class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.district_id = ''
        self.number = ''
        self.name = ''

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


class Factory(Base.Factory):

    """ Subdistrict Factory """

    @staticmethod
    def _get_object_class():
        return Subdistrict

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Subdistrict objects """

    @staticmethod
    def _get_table_name():
        return 'Subdistrict'
