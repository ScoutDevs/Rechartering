""" SponsoringOrganizations classes """
from . import Base


class SponsoringOrganizations(Base.Object):

    """ SponsoringOrganizations class """

    @staticmethod
    def get_uuid_prefix():
        return 'spo'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ SponsoringOrganization validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'subdistrict_id': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }

    @staticmethod
    def get_field_types():
        return {
            'uuid': str,
            'subdistrict_id': str,
            'name': str,
        }


class Factory(Base.Factory):

    """ SponsoringOrganizations Factory """

    @staticmethod
    def _get_object_class():
        return SponsoringOrganizations

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists SponsoringOrganizations objects """

    @staticmethod
    def _get_table_name():
        return 'SponsoringOrganizations'
