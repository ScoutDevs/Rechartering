""" AdultApplications classes """
from . import Base


class AdultApplications(Base.Object):

    """ AdultApplications class """

    @staticmethod
    def get_uuid_prefix():
        return 'aap'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ AdultApplication validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'org_id': Base.FIELD_REQUIRED,
            'data': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'status': str,
            'org_id': str,
            'data': dict,
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
