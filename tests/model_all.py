# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests models"""

import unittest

from models import COUNCIL_ID
from models import AdultApplications
from models import CharterApplications
from models import Guardian
from models import SponsoringOrganization
from models import Unit
from models import User
from models import Volunteer
from models import Youth

from . import FakeSponsoringOrganizationFactory
from . import FakeYouthFactory
from . import FakeYouthPersister


class ModelTestCase(unittest.TestCase):

    """Parent for all model tests"""

    def _set_up(self, module, obj_data):
        """Set up for all children"""
        self.factory = module.Factory()
        self.obj = self.factory.construct(obj_data)
        self.validator = self.obj.get_validator()

    def test_validation(self):
        """Test object validation"""
        if hasattr(self, 'obj'):
            self.assertTrue(self.validator.valid())


class TestUser(ModelTestCase):

    """Tests User model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'username': 'foo',
            'password': 'bar',
        }
        self._set_up(User, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('usr', self.obj.uuid[0:3])

    def test_password(self):
        """Make sure passwords are being hashed correctly"""
        hashed_password = '0f1128046248f83dc9b9ab187e16fad0ff596128f1524d05a9a77c4ad932f10a'
        self.assertEquals(hashed_password, self.obj.hash_password('howdy'))


class TestYouth(ModelTestCase):
    """Tests Youth model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'duplicate_hash': 'foo',
            'units': ['123', '456'],
            'first_name': 'Test',
            'last_name': 'McTesterton',
            'date_of_birth': '2000-01-01',
        }
        self.factory = FakeYouthFactory()
        self.obj = self.factory.construct(obj_data)
        self.persister = FakeYouthPersister()
        self.validator = self.obj.get_validator()

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('yth', self.obj.uuid[0:3])

    def test_duplicate_search(self):
        """Test duplicate check"""
        obj_data = {
            'duplicate_hash': 'foo',
            'units': ['123', '456'],
            'first_name': 'Matthew',
            'last_name': 'Reece',
            'date_of_birth': '2002-01-15',
        }

        obj = self.factory.construct(obj_data)
        duplicates = self.persister.find_potential_duplicates(obj)
        self.assertNotEqual(0, len(duplicates))

        obj.date_of_birth = '1970-01-02'
        duplicates = self.persister.find_potential_duplicates(obj)
        self.assertEqual(0, len(duplicates))


class TestVolunteer(ModelTestCase):

    """Tests Volunteer model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'scoutnet_id': 123,
            'unit_id': 'unt-123',
            'duplicate_hash': '123123123',
            'ypt_completion_date': '2015-01-01',
            'ssn': '123-45-6789',
            'first_name': 'Test',
            'last_name': "O'Test",
        }
        self._set_up(Volunteer, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('vol', self.obj.uuid[0:3])


class TestGuardian(ModelTestCase):

    """Tests Guardian model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'uuid': 'gdn-TEST-1',
            'youth': [123, 456],
            'first_name': 'Test',
            'last_name': 'Testerson',
        }
        self._set_up(Guardian, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('gdn', self.obj.uuid[0:3])


class TestSponsoringOrganization(ModelTestCase):

    """Tests SponsoringOrganization model"""

    def setUp(self):
        """Init"""
        obj_data = FakeSponsoringOrganizationFactory().load_by_uuid('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID).to_dict()
        self._set_up(SponsoringOrganization, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('spo', self.obj.uuid[0:3])


class TestUnit(ModelTestCase):

    """Tests Unit model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'parent_uuid': '123123',
            'type': 'Unit',
            'name': 'Troop',
            'number': 1455,
        }
        self._set_up(Unit, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('unt', self.obj.uuid[0:3])


class TestYouthApplication(ModelTestCase):

    """Tests Youth Application model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'status': Youth.APPLICATION_STATUS_COMPLETE,
            'unit_id': 'unt-123',
            'scoutnet_id': 123,
            'first_name': 'Ben',
            'last_name': 'Reece',
            'date_of_birth': '1980-01-01',
        }
        self.factory = Youth.ApplicationFactory()
        self.obj = self.factory.construct(obj_data)
        self.validator = self.obj.get_validator()

    def test_validation(self):
        """Overriding general validation to do status-specific validation"""
        pass

    def test_persistence(self):
        """Overriding general validation to do status-specific validation"""
        pass

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('yap', self.obj.uuid[0:3])

    def test_guardian_signature(self):
        """Test guardian signature validation"""
        self.obj.status = Youth.APPLICATION_STATUS_UNIT_APPROVAL
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_unit_approval(self):
        """Test unit approval validation"""
        self.obj.status = Youth.APPLICATION_STATUS_FEE_PENDING
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_fee_payment(self):
        """Test fee payment validation"""
        self.obj.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_record(self):
        """Test ready for ScoutNet validation"""
        self.obj.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_complete(self):
        """Test complete status"""
        self.obj.status = Youth.APPLICATION_STATUS_COMPLETE
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.obj.recorded_in_scoutnet_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_rejected(self):
        """Test reject status"""
        self.obj.status = Youth.APPLICATION_STATUS_REJECTED
        self.assertFalse(self.validator.valid())
        self.obj.rejection_date = '2015-01-01'
        self.obj.rejection_reason = 'stuff'
        self.assertTrue(self.validator.valid())


class TestAdultApplications(ModelTestCase):

    """Tests AdultApplications model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'status': 'Completed',
            'org_id': '123123',
        }
        self._set_up(AdultApplications, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('aap', self.obj.uuid[0:3])


class TestCharterApplications(ModelTestCase):
    """Tests CharterApplications model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'sponsoring_organization_id': '123123',
            'year': 2015,
            'status': 'Completed',
        }
        self._set_up(CharterApplications, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('cap', self.obj.uuid[0:3])


if __name__ == '__main__':
    unittest.main()
