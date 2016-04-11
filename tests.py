# pylint: disable=no-member,attribute-defined-outside-init
""" Tests everything! """

import unittest
import shortuuid
import sys
from controllers import InvalidActionException
from controllers import YouthApplication
from models import AdultApplications
from models import Base
from models import CharterApplications
from models import District
from models import Guardian
from models import SponsoringOrganization
from models import Subdistrict
from models import Unit
from models import User
from models import Volunteer
from models import Youth
from models import YouthApplications

ENVIRONMENT = 'dev'  # 'dev-persist' for persistence tests


class TestYouthApplication(unittest.TestCase):
    """ Test YouthApplication controller """

    def setUp(self):
        app_data = self.get_test_app_data()
        self.app = YouthApplications.Factory().construct(app_data)

        application_persister = TestYouthApplicationsPersister()
        unit_factory = TestUnitFactory()
        self.controller = YouthApplication.YouthApplication(
            application_persister,
            unit_factory
        )

    @staticmethod
    def get_test_app_data():
        """ Test YouthApplications data """
        return {
            'unit_id': 'unt-TEST-123',
            'scoutnet_id': 123,
            'data': {}
        }

    @staticmethod
    def get_test_youth_data():
        """ test Youths data """
        return {
            'uuid': 'yth-TEST-1',
            'first_name': 'Matthew',
            'last_name': 'Reece',
            'date_of_birth': '2002-01-15',
            'units': ['unt-TEST-123'],
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcde',
        }

    @staticmethod
    def get_test_unit_data():
        """ Test Unit data """
        return [
            {
                'uuid': 'unt-TEST-51',
                'sponsoring_organization_id': 'spo-TEST-51',
                'type': Unit.TYPE_TROOP,
                'number': 51,
                'lds_unit': False,
            },
            {
                'uuid': 'unt-TEST-123',
                'sponsoring_organization_id': 'spo-TEST-123',
                'type': Unit.TYPE_TROOP,
                'number': 1455,
                'lds_unit': True,
            },
        ]

    def test_youth_lookup(self):
        """ Test find_duplicate_youth method """
        if ENVIRONMENT == 'dev-persist':
            data = self.__class__.get_test_youth_data()
            duplicates = self.controller.find_duplicate_youth(data)
            self.assertNotEqual(0, len(duplicates))

            data['first_name'] = shortuuid.uuid()
            duplicates = self.controller.find_duplicate_youth(data)
            self.assertEqual(0, len(duplicates))

    def test_status_search(self):
        """ Test get_applications_by_status() """
        app_list = self.controller.get_applications_by_status(YouthApplications.STATUS_CREATED)
        self.assertNotEqual(0, len(app_list))

    def test_new_youth(self):
        """ Test new youth workflow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(YouthApplications.STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(YouthApplications.STATUS_UNIT_APPROVAL, self.app.status)

        unit_approval = {
            'unit_approval_user_id': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_approval(self.app, unit_approval)
        self.assertEqual(YouthApplications.STATUS_READY_FOR_SCOUTNET, self.app.status)

        recording_data = {
            'scoutnet_id': 123,
        }
        self.app = self.controller.mark_as_recorded(self.app, recording_data)
        self.assertEqual(YouthApplications.STATUS_COMPLETE, self.app.status)

    def test_guardian_approval_on_file(self):
        """ Test workflow when the guardian approval is on file """
        if ENVIRONMENT == 'dev-persist':
            data = self.__class__.get_test_youth_data()
            self.app.youth_id = data['uuid']
            self.app = self.controller.submit_application(self.app)
            self.assertEqual(YouthApplications.STATUS_UNIT_APPROVAL, self.app.status)

    def test_non_lds_flow(self):
        """ Test flow with non-LDS unit """
        if ENVIRONMENT == 'dev-persist':
            self.app.unit_id = 'unt-TEST-51'
            self.app = self.controller.submit_application(self.app)
            self.assertEqual(YouthApplications.STATUS_GUARDIAN_APPROVAL, self.app.status)

            guardian_approval = {
                'guardian_approval_guardian_id': 'grd-TEST-123',
                'guardian_approval_signature': 'abcd',
            }
            self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
            self.assertEqual(YouthApplications.STATUS_UNIT_APPROVAL, self.app.status)

            unit_approval = {
                'unit_approval_user_id': 'usr-TEST-123',
                'unit_approval_signature': 'abcd',
            }
            self.app = self.controller.submit_unit_approval(self.app, unit_approval)
            self.assertEqual(YouthApplications.STATUS_FEE_PENDING, self.app.status)

            fee_data = {
                'fee_payment_user_id': 'usr-TEST-123',
                'fee_payment_receipt': 123
            }
            self.app = self.controller.pay_fees(self.app, fee_data)
            self.assertEqual(YouthApplications.STATUS_READY_FOR_SCOUTNET, self.app.status)

            recording_data = {
                'scoutnet_id': 123,
            }
            self.app = self.controller.mark_as_recorded(self.app, recording_data)
            self.assertEqual(YouthApplications.STATUS_COMPLETE, self.app.status)

    def test_guardian_rejection(self):
        """ Test guardian rejection flow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(YouthApplications.STATUS_GUARDIAN_APPROVAL, self.app.status)

        data = {}
        self.app = self.controller.submit_guardian_rejection(self.app, data)
        self.assertEqual(YouthApplications.STATUS_REJECTED, self.app.status)

    def test_unit_rejection(self):
        """ Test unit rejection flow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(YouthApplications.STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(YouthApplications.STATUS_UNIT_APPROVAL, self.app.status)

        data = {
            'unit_approval_user_id': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_rejection(self.app, data)
        self.assertEqual(YouthApplications.STATUS_REJECTED, self.app.status)

    def test_invalid_workflows(self):
        """ Test invalid workflow exceptions """
        with self.assertRaises(InvalidActionException):
            guardian_approval = {
                'guardian_approval_guardian_id': 'grd-TEST-123',
                'guardian_approval_signature': 'abcd',
            }
            self.controller.submit_guardian_approval(self.app, guardian_approval)

        with self.assertRaises(InvalidActionException):
            unit_approval = {
                'unit_approval_user_id': 'usr-TEST-123',
                'unit_approval_signature': 'abcd',
            }
            self.controller.submit_unit_approval(self.app, unit_approval)

        with self.assertRaises(InvalidActionException):
            recording_data = {
                'scoutnet_id': 123,
            }
            self.app = self.controller.mark_as_recorded(self.app, recording_data)

        with self.assertRaises(InvalidActionException):
            self.app = self.controller.submit_application(self.app)
            self.controller.submit_application(self.app)


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


class TestVolunteer(ModelTestCase):

    """ Tests Volunteer module """

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
        self._set_up(Volunteer, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('vol', self.obj.uuid[0:3])


class TestGuardian(ModelTestCase):

    """ Tests Guardian module """

    def setUp(self):
        """ Init """
        obj_data = {
            'uuid': 'gdn-TEST-1',
            'youth': [123, 456],
            'first_name': 'Test',
            'last_name': 'Testerson',
        }
        self._set_up(Guardian, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('gdn', self.obj.uuid[0:3])


class TestDistrict(ModelTestCase):

    """ Tests District module """

    def setUp(self):
        """ Init """
        obj_data = {
            'number': '05',
            'name': 'Provo Peak',
        }
        self._set_up(District, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('dst', self.obj.uuid[0:3])


class TestSubdistrict(ModelTestCase):

    """ Tests Subdistrict module """

    def setUp(self):
        """ Init """
        obj_data = {
            'district_id': '123123',
            'number': '05-9',
            'name': 'Provo North Park Stake',
        }
        self._set_up(Subdistrict, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('sbd', self.obj.uuid[0:3])


class TestSponsoringOrganization(ModelTestCase):

    """ Tests SponsoringOrganization module """

    def setUp(self):
        """ Init """
        obj_data = {
            'subdistrict_id': '123123',
            'name': 'North Park 3rd Ward',
        }
        self._set_up(SponsoringOrganization, obj_data)

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('spo', self.obj.uuid[0:3])


class TestUnit(ModelTestCase):

    """ Tests Unit module """

    def setUp(self):
        """ Init """
        obj_data = {
            'sponsoring_organization_id': '123123',
            'type': 'Troop',
            'number': 1455,
        }
        self._set_up(Unit, obj_data)

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


def init_data():
    """ Create records in DB for testing """
    if ENVIRONMENT == 'dev-persist':
        data = TestYouthApplication.get_test_youth_data()
        youth = Youth.Factory().construct(data)
        Youth.Persister().save(youth)

        units = TestYouthApplication.get_test_unit_data()
        for unit_data in units:
            unit = Unit.Factory().construct(unit_data)
            Unit.Persister().save(unit)


def clear_data():
    """ Clean up test data """
    if ENVIRONMENT == 'dev-persist':
        data = TestYouthApplication.get_test_youth_data()
        youth = Youth.Factory().construct(data)
        Youth.Persister().delete(youth)

        units = TestYouthApplication.get_test_unit_data()
        for unit_data in units:
            unit = Unit.Factory().construct(unit_data)
            Unit.Persister().delete(unit)


class TestUnitFactory(object):

    def load_by_uuid(self, uuid):
        unit_data = TestYouthApplication.get_test_unit_data()
        return Unit.Factory().construct(unit_data[1])


class TestYouthApplicationsPersister(object):

    def get_by_status(self, status):
        test_data = TestYouthApplication.get_test_app_data()
        return [YouthApplications.Factory().construct(test_data)]


if __name__ == '__main__':
    init_data()
    unittest.main()
    clear_data()
