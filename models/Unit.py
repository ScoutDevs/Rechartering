"""Unit classes"""
from . import Base
from . import Organization

TYPE_PACK = 'Pack'
TYPE_TROOP = 'Troop'
TYPE_TEAM = 'Team'
TYPE_CREW = 'Crew'
TYPE_SHIP = 'Ship'
TYPE_POST = 'Post'


class Unit(Organization.Object):
    """Unit class"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.type = Organization.ORG_TYPE_UNIT
        self.parent_uuid = ''
        self.name = ''
        self.lds_unit = True
        self.number = ''

    def get_validator(self):
        return Validator(self)

    @staticmethod
    def get_uuid_prefix():
        return 'unt'


class Validator(Organization.Validator):
    """Unit validator"""

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'type': Base.FIELD_REQUIRED,
            'name': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
        }

    def _validate(self):
        valid_types = [
            TYPE_PACK,
            TYPE_TROOP,
            TYPE_TEAM,
            TYPE_CREW,
            TYPE_SHIP,
            TYPE_POST,
        ]
        valid = True
        errors = []

        if 'name' in self.obj.to_dict() and self.obj.name not in valid_types:
            errors.append('Invalid name "{}"; valid names: {}'.format(
                self.obj.name,
                ", ".join(valid_types)
                ))
            valid = False

        return (valid, errors)


class Factory(Base.Factory):
    """Unit Factory"""

    @staticmethod
    def _get_object_class():
        return Unit

    @staticmethod
    def get_persister():
        return Persister()


class Persister(Base.Persister):

    """Persists Unit objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
