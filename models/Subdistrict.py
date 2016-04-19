"""Subdistrict classes"""
from . import Base
from . import Organization
from . import RecordNotFoundException


class Subdistrict(Base.Object):
    """Subdistrict class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.type = Organization.ORG_TYPE_SUBDISTRICT
        self.parent_uuid = ''
        self.number = ''
        self.name = ''

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_factory():
        return Factory()


class Validator(Base.Validator):
    """Subdistrict Validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'type': Base.FIELD_REQUIRED,
            'parent_uuid': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """Subdistrict Factory"""

    @staticmethod
    def get_uuid_prefix():
        return 'sbd'

    @staticmethod
    def _get_object_class():
        return Subdistrict

    @staticmethod
    def _get_persister():
        return Persister()

    def get_from_file_data(self, data, district):
        """Load or create object from file dict"""
        try:
            obj = self.load_from_database_query(
                {
                    '__index__': 'number',
                    'type': Organization.ORG_TYPE_SUBDISTRICT,
                    'number': district.number + '-' + data['Sub District #'],
                }
            )
        except RecordNotFoundException:
            klass = self._get_object_class()
            obj = klass()
            obj.number = district.number + '-' + data['Sub District #']
            obj.name = data['Stake/Sub District Name']
            obj.parent_uuid = district.uuid
            obj.validate()
        return obj


class Persister(Base.Persister):

    """Persists Subdistrict objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
