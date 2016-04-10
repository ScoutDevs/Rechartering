# pylint: disable=no-member,attribute-defined-outside-init
""" Tests models package """

import unittest
import sys
from . import Base
from . import User
from . import Youth
from . import Volunteers
from . import Guardians
from . import Districts
from . import Subdistricts
from . import SponsoringOrganizations
from . import Units
from . import YouthApplications
from . import AdultApplications
from . import CharterApplications


ENVIRONMENT = 'dev'  # 'dev-persist' to test with persistence


class ModelTestCase(unittest.TestCase):

    """ Parent for all model tests """

    def _set_up(self, module, obj_data):
        """ Set up for all children """
        self.factory = module.Factory()
        self.obj = self.factory.construct(obj_data)
        self.persister = module.Persister()
        self.validator = self.obj.get_validator()

    def test_persistence(self):
        """ Test persistence of object """
        if hasattr(self, 'obj') and ENVIRONMENT == 'dev-persist':
            self.persister.save(self.obj)

            new_obj = self.factory.load_by_uuid(self.obj.uuid)
            self.assertEquals(new_obj.uuid, self.obj.uuid)

            self.persister.delete(self.obj)
            with self.assertRaises(Base.RecordNotFoundException):
                self.factory.load_by_uuid(self.obj.uuid)

    def test_validation(self):
        """ Test object validation """
        if hasattr(self, 'obj'):
            self.assertTrue(self.validator.valid())


class TestUser(ModelTestCase):

    """ Tests User module """

    def setUp(self):
        """ Init """
        obj_data = {
            'username': 'foo',
            'password': 'bar',
        }
        self._set_up(User, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('usr', self.obj.uuid[0:3])

    def test_field_type_validation(self):
        """ Ensure field type validation is occurring """
        self.obj.roles = 'test'
        if 1 in sys.argv and sys.argv[1] == '--test-persistence':
            with self.assertRaises(Base.InvalidObjectException):
                self._test_persistence()

    def test_password(self):
        """ Make sure passwords are being hashed correctly """
        hashed_password = '0f1128046248f83dc9b9ab187e16fad0ff596128f1524d05a9a77c4ad932f10a'
        self.assertEquals(hashed_password, self.obj.hash_password('howdy'))


class TestYouth(ModelTestCase):

    """ Tests Youth module """

    def setUp(self):
        """ Init """
        obj_data = {
            'duplicate_hash': 'foo',
            'units': [123, 456],
            'first_name': 'Test',
            'last_name': 'McTesterton',
            'date_of_birth': '2000-01-01',
        }
        self._set_up(Youth, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('yth', self.obj.uuid[0:3])

    def test_duplicate_search(self):
        """ Test duplicate check """
        if ENVIRONMENT == 'dev-persist':
            obj_data = {
                'duplicate_hash': 'foo',
                'units': [123, 456],
                'first_name': 'Test',
                'last_name': 'McTesterton',
                'date_of_birth': '2000-01-01',
            }

            original_obj = self.factory.construct(obj_data)
            self.persister.save(original_obj)

            duplicate_obj = self.factory.construct(obj_data)
            duplicates = self.persister.find_potential_duplicates(duplicate_obj)
            self.assertNotEqual(0, len(duplicates))

            duplicate_obj.date_of_birth = '1970-01-02'
            duplicates = self.persister.find_potential_duplicates(duplicate_obj)
            self.assertEqual(0, len(duplicates))

            self.persister.delete(original_obj)


class TestVolunteers(ModelTestCase):

    """ Tests Volunteers module """

    def setUp(self):
        """ Init """
        obj_data = {
            'scoutnet_id': 123,
            'unit_id': 'unt-123',
            'duplicate_hash': '123123123',
            'ypt_completion_date': '2015-01-01',
            'ssn': '123-45-6789',
            'first_name': 'Test',
            'last_name': "O'Test",
        }
        self._set_up(Volunteers, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('vol', self.obj.uuid[0:3])


class TestGuardians(ModelTestCase):

    """ Tests Guardians module """

    def setUp(self):
        """ Init """
        obj_data = {
            'uuid': 'gdn-TEST-1',
            'youth': [123, 456],
            'first_name': 'Test',
            'last_name': 'Testerson',
        }
        self._set_up(Guardians, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('gdn', self.obj.uuid[0:3])


class TestDistricts(ModelTestCase):

    """ Tests Districts module """

    def setUp(self):
        """ Init """
        obj_data = {
            'number': '05',
            'name': 'Provo Peak',
        }
        self._set_up(Districts, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('dst', self.obj.uuid[0:3])


class TestSubdistricts(ModelTestCase):

    """ Tests Subdistricts module """

    def setUp(self):
        """ Init """
        obj_data = {
            'district_id': '123123',
            'number': '05-9',
            'name': 'Provo North Park Stake',
        }
        self._set_up(Subdistricts, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('sbd', self.obj.uuid[0:3])


class TestSponsoringOrganizations(ModelTestCase):

    """ Tests SponsoringOrganizations module """

    def setUp(self):
        """ Init """
        obj_data = {
            'subdistrict_id': '123123',
            'name': 'North Park 3rd Ward',
        }
        self._set_up(SponsoringOrganizations, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('spo', self.obj.uuid[0:3])


class TestUnits(ModelTestCase):

    """ Tests Units module """

    def setUp(self):
        """ Init """
        obj_data = {
            'sponsoring_organization_id': '123123',
            'type': 'Troop',
            'number': 1455,
        }
        self._set_up(Units, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('unt', self.obj.uuid[0:3])


class TestYouthApplications(ModelTestCase):

    """ Tests YouthApplications module """

    def setUp(self):
        """ Init """
        obj_data = {
            'status': YouthApplications.STATUS_COMPLETE,
            'unit_id': 'unt-123',
            'scoutnet_id': 123,
            'data': {}
        }
        self._set_up(YouthApplications, obj_data)

    def test_validation(self):
        """ Overriding general validation to do status-specific validation """
        pass

    def test_persistence(self):
        """ Overriding general validation to do status-specific validation """
        pass

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('yap', self.obj.uuid[0:3])

    def test_guardian_signature(self):
        """ Test guardian signature validation """
        self.obj.status = YouthApplications.STATUS_UNIT_APPROVAL
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_unit_approval(self):
        """ Test unit approval validation """
        self.obj.status = YouthApplications.STATUS_FEE_PENDING
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_fee_payment(self):
        """ Test fee payment validation """
        self.obj.status = YouthApplications.STATUS_READY_FOR_SCOUTNET
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_record(self):
        """ Test ready for ScoutNet validation """
        self.obj.status = YouthApplications.STATUS_READY_FOR_SCOUTNET
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_complete(self):
        """ Test complete status """
        self.obj.status = YouthApplications.STATUS_COMPLETE
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
        """ Test reject status """
        self.obj.status = YouthApplications.STATUS_REJECTED
        self.assertFalse(self.validator.valid())
        self.obj.rejection_date = '2015-01-01'
        self.obj.rejection_reason = 'stuff'
        self.assertTrue(self.validator.valid())


class TestAdultApplications(ModelTestCase):

    """ Tests AdultApplications module """

    def setUp(self):
        """ Init """
        obj_data = {
            'status': 'Completed',
            'org_id': '123123',
            'data': {},
        }
        self._set_up(AdultApplications, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('aap', self.obj.uuid[0:3])


class TestCharterApplications(ModelTestCase):

    """ Tests CharterApplications module """

    def setUp(self):
        """ Init """
        obj_data = {
            'sponsoring_organization_id': '123123',
            'year': 2015,
            'status': 'Completed',
        }
        self._set_up(CharterApplications, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('cap', self.obj.uuid[0:3])


if __name__ == '__main__':
    unittest.main()
