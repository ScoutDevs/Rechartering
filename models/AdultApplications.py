"""AdultApplications classes"""
from . import Base


# TO-DO: encrypt & clean out SSNs


class AdultApplications(Base.Object):
    """AdultApplications class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.uuid = self.get_uuid()
        self.status = ''
        self.org_uuid = ''
        self.data = {}

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'aap'


class Validator(Base.Validator):
    """AdultApplication validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'org_uuid': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """AdultApplications Factory"""

    @staticmethod
    def _get_object_class():
        return AdultApplications

    @staticmethod
    def get_persister():
        return Persister()


class Persister(Base.Persister):
    """Persists AdultApplications objects"""

    @staticmethod
    def _get_table_name():
        return 'Applications'
