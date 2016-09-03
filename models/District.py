"""District classes"""
from . import COUNCIL_ID
from . import Base
from . import Organization
from . import RecordNotFoundException


class District(Organization.Object):
    """District class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.type = Organization.ORG_TYPE_DISTRICT
        self.parent_uuid = 'cnl-'+COUNCIL_ID

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'dst'


class Validator(Base.Validator):
    """District validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'type': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """District Factory"""

    @staticmethod
    def _get_object_class():
        return District

    @staticmethod
    def get_persister():
        return Persister()

    def get_from_file_data(self, data):
        """Load or create object from file dict"""
        try:
            obj = self.load_from_database_query(
                {
                    '__index__': 'number',
                    'number': data['district_number'].strip(),
                    'type': Organization.ORG_TYPE_DISTRICT,
                }
            )
        except RecordNotFoundException:
            klass = self._get_object_class()
            obj = klass()
        obj.number = data['district_number'].strip()
        obj.name = data['district_name'].strip()
        obj.validate()
        return obj


class Persister(Base.Persister):
    """Persists District objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
