# pylint: disable=import-error
"""Organization Controller"""
import Security
from models import District
from models import Organization
from models import RecordNotFoundException
from models import SponsoringOrganization
from models import Subdistrict
from models import Unit

from . import ClientErrorException
from .Security import require_role


class Controller(object):
    """Organization CRUD Controller

    'Organization' in this case includes units, districts, subdistricts, and
    sponsoring organizations.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 user,
                 district_factory=None,
                 subdistrict_factory=None,
                 sporg_factory=None,
                 unit_factory=None,
                 organization_persister=None):
        self.user = user

        if district_factory:
            self.district_factory = district_factory
        else:
            self.district_factory = District.Factory()
        if subdistrict_factory:
            self.subdistrict_factory = subdistrict_factory
        else:
            self.subdistrict_factory = Subdistrict.Factory()
        if sporg_factory:
            self.sporg_factory = sporg_factory
        else:
            self.sporg_factory = SponsoringOrganization.Factory()
        if unit_factory:
            self.unit_factory = unit_factory
        else:
            self.unit_factory = Unit.Factory()
        if organization_persister:
            self.organization_persister = organization_persister
        else:
            self.organization_persister = Organization.Persister()

    def get(self, uuid):
        """Get

        Args:
            uuid: string
        Returns:
            Organization object (District, Subdistrict, sporg,
            or Unit object)
        """
        return self._get_factory_by_uuid(uuid).load_by_uuid(uuid)

    @require_role(Security.ROLE_COUNCIL_ADMIN)
    def set(self, data):
        """Record-level create/update

        Args:
            data: dict containing the org data; will REPLACE any existing
                record in its entirety
        Returns:
            Updated Organization object (District, Subdistrict,
                sporg, or Unit object)
        """
        if 'type' in data:
            obj = self._get_factory_by_type(data['type']).construct(data)
            obj.validate()
            return obj
        else:
            raise ClientErrorException('Invalid organization type specified.')

    @require_role(Security.ROLE_COUNCIL_ADMIN)
    def update(self, data):
        """Field-level create/update

        Args:
            data: dict containing the org data to update; will MODIFY any
                existing record
        Returns:
            Updated Organization object (District, Subdistrict,
                sporg, or Unit object)
        """
        if 'uuid' in data:
            obj = self._get_factory_by_uuid(data['uuid']).load_by_uuid(data['uuid'])
            obj.set_from_data(data)
            obj.validate()
            return obj
        else:
            raise ClientErrorException('No uuid specified.')

    def search(self, search_data):
        """Find

        Args:
            search_data: dict containing data to search for
        Returns:
            list of Organization dicts
        """
        return self.organization_persister.query(search_data)

    def _get_factory_by_type(self, org_type):
        """Determines which model factory to use

        Args:
            type: string
        Returns:
            Factory object
        """
        if org_type == Organization.ORG_TYPE_UNIT:
            factory = self.unit_factory
        elif org_type == Organization.ORG_TYPE_SPONSORING_ORGANIZATION:
            factory = self.sporg_factory
        elif org_type == Organization.ORG_TYPE_SUBDISTRICT:
            factory = self.subdistrict_factory
        elif org_type == Organization.ORG_TYPE_DISTRICT:
            factory = self.district_factory
        else:
            raise ClientErrorException('Invalid organization type')
        return factory

    def _get_factory_by_uuid(self, uuid):
        """Determines which model factory to use

        Args:
            uuid: string
        Returns:
            Factory object
        """
        for factory in self._get_factories():
            if uuid[0:3] == factory.get_uuid_prefix():
                return factory
        raise RecordNotFoundException('Invalid UUID')

    def _get_factories(self):
        """Returns list of all applicable factories

        Returns:
            list
        """
        return [
            self.district_factory,
            self.subdistrict_factory,
            self.sporg_factory,
            self.unit_factory,
        ]
