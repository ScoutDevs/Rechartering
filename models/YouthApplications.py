""" YouthApplications classes """
from . import Base


class YouthApplications(Base.Object):

    """ YouthApplications class """

    @staticmethod
    def get_uuid_prefix():
        return 'yap'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'unit_id': Base.FIELD_REQUIRED,
            'data': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ YouthApplications Factory """

    @staticmethod
    def _get_object_class():
        return YouthApplications

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists YouthApplications objects """

    @staticmethod
    def _get_table_name():
        return 'YouthApplications'
