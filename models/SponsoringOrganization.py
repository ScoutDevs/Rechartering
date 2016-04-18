"""SponsoringOrganization classes"""
from . import Base


class SponsoringOrganization(Base.Object):
    """SponsoringOrganization class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.type = ''
        self.parent_uuid = ''
        self.subdistrict_id = ''
        self.name = ''

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_factory():
        return Factory()


class Validator(Base.Validator):
    """SponsoringOrganization validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'subdistrict_id': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """SponsoringOrganization Factory"""

    @staticmethod
    def get_uuid_prefix():
        return 'spo'

    @staticmethod
    def _get_object_class():
        return SponsoringOrganization

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """Persists SponsoringOrganization objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
