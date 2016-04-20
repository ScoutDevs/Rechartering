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
                    'number': data['subdistrict_number'].strip(),
                }
            )
        except RecordNotFoundException:
            klass = self._get_object_class()
            obj = klass()
        obj.number = data['subdistrict_number'].strip()
        obj.name = data['subdistrict_name'].strip()
        obj.parent_uuid = district.uuid
        obj.validate()
        return obj


class Persister(Base.Persister):

    """Persists Subdistrict objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
