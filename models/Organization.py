"""Organization classes"""
from . import Base

ORG_TYPE_DISTRICT = 'District'
ORG_TYPE_SUBDISTRICT = 'Subdistrict'
ORG_TYPE_SPONSORING_ORGANIZATION = 'Sponsoring Organization'
ORG_TYPE_UNIT = 'Unit'


class Persister(Base.Persister):

    """Persists Unit objects"""

    @staticmethod
    def _get_table_name():
        return 'Organizations'
