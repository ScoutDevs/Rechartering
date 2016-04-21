"""Organization classes"""
from . import Base

ORG_TYPE_DISTRICT = 'District'
ORG_TYPE_SUBDISTRICT = 'Subdistrict'
ORG_TYPE_SPONSORING_ORGANIZATION = 'Sponsoring Organization'
ORG_TYPE_UNIT = 'Unit'


class Object(Base.Object):
    """Base Organization class"""

    def __init__(self):
        super(Object, self).__init__()
        self.name = ''
        self.parent_uuid = ''
        self._number = None
        self._uuid = None

    @property
    def number(self):
        """number property"""
        return self._number

    @number.setter
    def number(self, value):
        """number property"""
        if not self._number or value == self._number:
            self._number = value
        else:
            raise Exception('Number cannot be changed once set')

    @property
    def uuid(self):
        """uuid property"""
        self._uuid = self.get_uuid()
        return self._uuid

    def to_dict(self):
        """Converts object to dict"""
        data = super(Object, self).to_dict()
        data['uuid'] = self.get_uuid()
        return data

    def get_uuid(self):
        """Generates a UUID"""
        if not self.number:
            raise Exception('Insufficient information to generate UUID')
        return '{}-{}.{}'.format(
            self.get_uuid_prefix(),
            self.number,
            self.parent_uuid,
        )


class Validator(Base.Validator):
    """Base validator for Organizations"""
    pass


class Persister(Base.Persister):

    """Persists Unit objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
