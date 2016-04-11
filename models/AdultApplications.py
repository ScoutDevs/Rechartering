""" AdultApplications classes """
from . import Base


class AdultApplications(Base.Object):
    """ AdultApplications class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.status = ''
        self.org_id = ''
        self.data = {}

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_factory():
        return Factory()


class Validator(Base.Validator):
    """ AdultApplication validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'org_id': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """ AdultApplications Factory """

    @staticmethod
    def _get_uuid_prefix():
        return 'aap'

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
