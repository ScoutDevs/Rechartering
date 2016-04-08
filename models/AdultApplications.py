""" AdultApplications classes """
from . import Base


class AdultApplications(Base.Object):

    """ AdultApplications class """

    @staticmethod
    def get_uuid_prefix():
        return 'aap'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'org_id': Base.FIELD_REQUIRED,
            'data': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ AdultApplications Factory """

    @staticmethod
    def _get_object_class():
        return AdultApplications

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists AdultApplications objects """

    @staticmethod
    def _get_table_name():
        return 'AdultApplications'
