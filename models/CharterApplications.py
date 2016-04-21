"""CharterApplications classes"""
from . import Base


class CharterApplications(Base.Object):
    """CharterApplications class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.uuid = self.get_uuid()
        self.sponsoring_organization_id = ''
        self.year = 0
        self.status = ''

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'cap'


class Validator(Base.Validator):

    """CharterApplication validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'sponsoring_organization_id': Base.FIELD_REQUIRED,
            'year': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):

    """CharterApplications Factory"""

    @staticmethod
    def _get_object_class():
        return CharterApplications

    @staticmethod
    def get_persister():
        return Persister()


class Persister(Base.Persister):

    """Persists CharterApplications objects"""

    @staticmethod
    def _get_table_name():
        return 'Applications'
