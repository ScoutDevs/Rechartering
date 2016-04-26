# pylint: disable=import-error
"""Guardian Controller"""
import Security
from models import Guardian

from . import ClientErrorException
from .Security import require_role


class Controller(object):
    """Guardian CRUD Controller

    A 'Guardian' is a parent or guardian of one or more youth.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 user,
                 factory=None):
        self.user = user

        if factory:
            self.factory = factory
        else:
            self.factory = Guardian.Factory()

    @require_role([Security.ROLE_COUNCIL_ADMIN, Security.ROLE_UNIT_ADMIN, Security.ROLE_GUARDIAN])
    def get(self, uuid):
        """Get

        Args:
            uuid: string
        Returns:
            object
        """
        return self.factory.load_by_uuid(uuid)

    @require_role([Security.ROLE_COUNCIL_ADMIN, Security.ROLE_UNIT_ADMIN, Security.ROLE_GUARDIAN])
    def set(self, data):
        """Record-level create/update

        Args:
            data: dict containing the data; will REPLACE any existing
                record in its entirety
        Returns:
            Updated object
        """
        obj = self.factory.construct(data)
        obj.validate()
        return obj

    @require_role([Security.ROLE_COUNCIL_ADMIN, Security.ROLE_UNIT_ADMIN, Security.ROLE_GUARDIAN])
    def update(self, data):
        """Field-level create/update

        Args:
            data: dict containing the org data to update; will MODIFY any
                existing record
        Returns:
            Updated object
        """
        if 'uuid' in data and data['uuid']:
            obj = self.factory.load_by_uuid(data['uuid'])
            obj.set_from_data(data)
            obj.validate()
            return obj
        else:
            raise ClientErrorException('No uuid specified.')

    @require_role([Security.ROLE_COUNCIL_ADMIN, Security.ROLE_UNIT_ADMIN, Security.ROLE_GUARDIAN])
    def search(self, search_data):
        """Find

        Args:
            search_data: dict containing data to search for
        Returns:
            list of dicts
        """
        return self.factory.get_persister().query(search_data)
