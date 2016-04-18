# pylint: disable=import-error
"""Organization Controller"""
from models import District
from models import Organization
from models import RecordNotFoundException
from models import SponsoringOrganization
from models import Subdistrict
from models import Unit


class Controller(object):
    """Organization CRUD Controller

    'Organization' in this case includes units, districts, subdistricts, and
    sponsoring organizations.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 district_factory=District.Factory(),
                 subdistrict_factory=Subdistrict.Factory(),
                 sponsoringorganization_factory=SponsoringOrganization.Factory(),
                 unit_factory=Unit.Factory(),
                 organization_persister=Organization.Persister()):
        self.district_factory = district_factory
        self.subdistrict_factory = subdistrict_factory
        self.sponsoringorganization_factory = sponsoringorganization_factory
        self.unit_factory = unit_factory
        self.organization_persister = organization_persister

    def get(self, uuid):
        """Get

        Args:
            uuid: string
        Returns:
            Organization object (District, Subdistrict, SponsoringOrganization,
            or Unit object)
        """
        return self._get_factory_by_uuid(uuid).load_by_uuid(uuid)

    def set(self, data):
        """Record-level create/update

        Args:
            data: dict containing the org data; will REPLACE any existing
                record in its entirety
        Returns:
            Updated Organization object (District, Subdistrict,
                SponsoringOrganization, or Unit object)
        """
        pass

    def update(self, data):
        """Field-level create/update

        Args:
            data: dict containing the org data to update; will MODIFY any
                existing record
        Returns:
            Updated Organization object (District, Subdistrict,
                SponsoringOrganization, or Unit object)
        """
        pass

    def search(self, search_data):
        """Find

        Args:
            search_data: dict containing data to search for
        Returns:
            list of Organization dicts
        """
        return self.organization_persister.query(search_data)

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
            self.sponsoringorganization_factory,
            self.unit_factory,
        ]
