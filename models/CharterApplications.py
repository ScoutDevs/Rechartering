""" CharterApplications classes """
from . import Base


class CharterApplications(Base.Object):

    """ CharterApplications class """

    @staticmethod
    def get_uuid_prefix():
        return 'cap'

    @staticmethod
    def get_fields():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'sponsoring_organization_id': Base.FIELD_REQUIRED,
            'year': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ CharterApplications Factory """

    @staticmethod
    def _get_object_class():
        return CharterApplications

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists CharterApplications objects """

    @staticmethod
    def _get_table_name():
        return 'CharterApplications'
