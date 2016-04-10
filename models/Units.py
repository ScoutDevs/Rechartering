""" Units classes """
from . import Base


class Units(Base.Object):

    """ Units class """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.sponsoring_organization_id = ''
        self.type = ''
        self.number = 0

    @staticmethod
    def get_uuid_prefix():
        return 'unt'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ Unit validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'sponsoring_organization_id': Base.FIELD_REQUIRED,
            'type': Base.FIELD_REQUIRED,
            'number': Base.FIELD_REQUIRED,
        }

    def _validate(self):
        valid_types = [
            'Pack',
            'Troop',
            'Team',
            'Crew',
            'Ship',
            'Post',
        ]
        valid = True
        errors = []

        if 'type' in self.obj.__dict__ and self.obj.type not in valid_types:
            errors.append('Invalid unit type "{}"; valid types: {}'.format(
                self.obj.type,
                ", ".join(valid_types)
                ))
            valid = False

        return (valid, errors)


class Factory(Base.Factory):

    """ Units Factory """

    @staticmethod
    def _get_object_class():
        return Units

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists Units objects """

    @staticmethod
    def _get_table_name():
        return 'Units'
