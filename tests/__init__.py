# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""General functionality for use across tests"""

from controllers import Security
from models import COUNCIL_ID
from models import Base
from models import District
from models import Guardian
from models import Organization
from models import Subdistrict
from models import SponsoringOrganization
from models import Unit
from models import User
from models import Youth


class FakePersister(object):
    """Fake persister"""

    def __init__(self, data):
        self.data = data

    def get(self, search_data):
        """Finds a test data record by the search_data"""
        record = None
        for item in self.data:
            match = True
            for field_name, field_value in search_data.items():
                if item[field_name] != field_value:
                    match = False
                    break
            if match:
                record = item
                break
        if record:
            return record
        else:
            raise Base.RecordNotFoundException('No record found that matches requested criteria.')

    def query(self, search_data):
        """Finds test data records matching the search_data"""
        records = []
        if '__index__' in search_data:
            del search_data['__index__']
        for item in self.data:
            match = True
            for field_name, field_value in search_data.items():
                if field_name not in item or item[field_name] != field_value:
                    match = False
                    break
            if match:
                records.append(item)
        return records


class FakeUserFactory(User.Factory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeUserPersister()


class FakeUserPersister(FakePersister):
    """Test persister"""

    def __init__(self):
        data = [
            {
                'uuid': 'usr-ben',
                'username': 'ben',
                'password': 'ben',
                'guardian_id': 'gdn-TEST-1',
                'roles': {
                    Security.ROLE_COUNCIL_ADMIN: [],
                },
            },
            {
                'uuid': 'usr-ken',
                'username': 'ken',
                'password': 'ken',
                'roles': {
                    Security.ROLE_GUARDIAN: [],
                },
            },
        ]
        super(FakeUserPersister, self).__init__(data)


class FakeGuardianFactory(Guardian.Factory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeGuardianPersister()


class FakeGuardianPersister(FakePersister):
    """Fake class for testing"""

    def __init__(self):
        data = [
            {
                'uuid': 'gdn-TEST-1',
                'user_uuid': 'usr-ben',
                'first_name': 'Ben',
                'last_name': 'Reece',
                'youth': ['yth-TEST-1'],
            },
        ]
        super(FakeGuardianPersister, self).__init__(data)


class FakeUnitFactory(Unit.Factory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeUnitPersister()


class FakeUnitPersister(FakePersister):
    """Test persister"""

    def __init__(self):
        super(FakeUnitPersister, self).__init__(self.get_test_data())

    @staticmethod
    def get_test_data():
        """Test data definition"""
        return [
            {
                'uuid': 'unt-51.spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_UNIT,
                'parent_uuid': 'spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID,
                'name': Unit.TYPE_TROOP,
                'number': '51',
                'lds_unit': False,
            },
            {
                'uuid': 'unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_UNIT,
                'parent_uuid': 'spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
                'name': Unit.TYPE_TROOP,
                'number': '1455',
                'lds_unit': True,
            },
        ]


class FakeDistrictFactory(District.Factory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeDistrictPersister()


class FakeDistrictPersister(FakePersister):
    """Test persister"""

    @staticmethod
    def get_test_data():
        """Test data definition"""
        return [
            {
                'uuid': 'dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_DISTRICT,
                'parent_uuid': 'cnl-'+COUNCIL_ID,
                'name': 'Provo Peak',
                'number': '5',
            },
        ]

    def __init__(self):
        super(FakeDistrictPersister, self).__init__(self.get_test_data())


class FakeSubdistrictFactory(Subdistrict.Factory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeSubdistrictPersister()


class FakeSubdistrictPersister(FakePersister):
    """Test persister"""

    @staticmethod
    def get_test_data():
        """Test data definition"""
        return [
            {
                'uuid': 'sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_SUBDISTRICT,
                'name': 'Provo North Park Stake',
                'number': '5-9',
                'parent_uuid': 'dst-5.cnl-'+COUNCIL_ID,
            },
            {
                'uuid': 'sbd-5-8.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_SUBDISTRICT,
                'name': 'Community Units',
                'number': '5-8',
                'parent_uuid': 'dst-5.cnl-'+COUNCIL_ID,
            },
        ]

    def __init__(self):
        super(FakeSubdistrictPersister, self).__init__(self.get_test_data())


class FakeSponsoringOrganizationFactory(SponsoringOrganization.Factory):  # pylint: disable=no-init,too-few-public-methods,line-too-long
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeSponsoringOrganizationPersister()


class FakeSponsoringOrganizationPersister(FakePersister):
    """Test persister"""

    @staticmethod
    def get_test_data():
        """Test data definition"""
        return [
            {
                'uuid': 'spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_SPONSORING_ORGANIZATION,
                'name': 'North Park 3rd Ward',
                'number': '1455',
                'parent_uuid': 'sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
            },
            {
                'uuid': 'spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID,
                'type': Organization.ORG_TYPE_SPONSORING_ORGANIZATION,
                'name': 'Provo Elks Lodge',
                'number': '51',
                'parent_uuid': 'sbd-5-8.dst-5.cnl-'+COUNCIL_ID,
            },
        ]

    def __init__(self):
        super(FakeSponsoringOrganizationPersister, self).__init__(self.get_test_data())


class FakeYouthApplicationFactory(Youth.ApplicationFactory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeYouthApplicationPersister()


class FakeYouthApplicationPersister(FakePersister):
    """Fake class for testing"""

    def __init__(self):
        data = [
            {
                'uuid': 'yap-TEST-1',
                'unit_id': 'unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
                'scoutnet_id': 123,
                'status': Youth.APPLICATION_STATUS_CREATED,
                'first_name': 'Ben',
                'last_name': 'Reece',
                'date_of_birth': '1970-01-01',
            },
        ]
        super(FakeYouthApplicationPersister, self).__init__(data)

    def get_by_status(self, status):
        """Fake method for testing"""
        return self.query({'status': status})


class FakeYouthFactory(Youth.YouthFactory):  # pylint: disable=too-few-public-methods,no-init
    """Fake class for testing"""

    @staticmethod
    def get_persister():
        """Get corresponding persister"""
        return FakeYouthPersister()


class FakeYouthPersister(FakePersister):
    """Fake class for testing"""

    def __init__(self):
        data = [
            {
                'uuid': 'yth-TEST-1',
                'first_name': 'Matthew',
                'last_name': 'Reece',
                'date_of_birth': '2002-01-15',
                'duplicate_hash': 'b94302d98d30a3e48ea80c7f4432a6f30661869f0a95e0096f50e84edc0fc09b',
                'units': ['unt-TEST-1455'],
                'guardian_approval_guardian_id': 'gdn-TEST-123',
                'guardian_approval_signature': 'abcde',
            },
            {
                'uuid': 'yth-TEST-2',
                'first_name': 'Jacob',
                'last_name': 'Reece',
                'scoutnet_id': '123',
                'date_of_birth': '2005-12-22',
                'duplicate_hash': '123',
                'units': ['unt-TEST-1455'],
                'guardian_approval_guardian_id': '',
                'guardian_approval_signature': '',
            },
        ]
        super(FakeYouthPersister, self).__init__(data)

    def find_potential_duplicates(self, youth):
        """Fake method for testing"""
        return self.query({'duplicate_hash': youth.get_record_hash()})


class FakeOrganizationPersister(FakePersister):
    """Test persister"""

    def __init__(self):
        data = \
            FakeUnitPersister.get_test_data() + \
            FakeDistrictPersister.get_test_data() + \
            FakeSubdistrictPersister.get_test_data() + \
            FakeSponsoringOrganizationPersister.get_test_data()
        super(FakeOrganizationPersister, self).__init__(data)
