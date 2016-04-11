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


class TestYouthApplicationController(unittest.TestCase):
    """ Test YouthApplicationController """

    def setUp(self):
        app_data = self.get_test_app_data()[0]
        self.app = Youth.ApplicationFactory().construct(app_data)

        application_persister = TestYouthApplicationPersister()
        unit_factory = TestUnitFactory()
        youth_factory = TestYouthFactory()
        youth_persister = TestYouthPersister()
        self.controller = YouthApplication.Controller(
            application_persister,
            unit_factory,
            youth_factory,
            youth_persister
        )

    @staticmethod
    def get_test_app_data():
        """ Test Youth Application data """
        return [
            {
                'unit_id': 'unt-TEST-123',
                'scoutnet_id': 123,
                'status': Youth.APPLICATION_STATUS_CREATED,
            },
        ]

    @staticmethod
    def get_test_youth_data():
        """ test Youths data """
        return [
            {
                'uuid': 'yth-TEST-1',
                'first_name': 'Matthew',
                'last_name': 'Reece',
                'date_of_birth': '2002-01-15',
                'duplicate_hash': 'b94302d98d30a3e48ea80c7f4432a6f30661869f0a95e0096f50e84edc0fc09b',
                'units': ['unt-TEST-123'],
                'guardian_approval_guardian_id': 'grd-TEST-123',
                'guardian_approval_signature': 'abcde',
            },
        ]

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
        data = self.__class__.get_test_youth_data()[0]
        duplicates = self.controller.find_duplicate_youth(data)
        self.assertNotEqual(0, len(duplicates))

        data['first_name'] = shortuuid.uuid()
        duplicates = self.controller.find_duplicate_youth(data)
        self.assertEqual(0, len(duplicates))

    def test_status_search(self):
        """ Test get_applications_by_status() """
        app_list = self.controller.get_applications_by_status(Youth.APPLICATION_STATUS_CREATED)
        self.assertNotEqual(0, len(app_list))

    def test_new_youth(self):
        """ Test new youth workflow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        unit_approval = {
            'unit_approval_user_id': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_approval(self.app, unit_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET, self.app.status)

        recording_data = {
            'scoutnet_id': 123,
        }
        self.app = self.controller.mark_as_recorded(self.app, recording_data)
        self.assertEqual(Youth.APPLICATION_STATUS_COMPLETE, self.app.status)

    def test_guardian_approval_on_file(self):
        """ Test workflow when the guardian approval is on file """
        data = self.__class__.get_test_youth_data()[0]
        self.app.youth_id = data['uuid']
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

    def test_non_lds_flow(self):
        """ Test flow with non-LDS unit """
        self.app.unit_id = 'unt-TEST-51'
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        unit_approval = {
            'unit_approval_user_id': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_approval(self.app, unit_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_FEE_PENDING, self.app.status)

        fee_data = {
            'fee_payment_user_id': 'usr-TEST-123',
            'fee_payment_receipt': 123
        }
        self.app = self.controller.pay_fees(self.app, fee_data)
        self.assertEqual(Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET, self.app.status)

        recording_data = {
            'scoutnet_id': 123,
        }
        self.app = self.controller.mark_as_recorded(self.app, recording_data)
        self.assertEqual(Youth.APPLICATION_STATUS_COMPLETE, self.app.status)

    def test_guardian_rejection(self):
        """ Test guardian rejection flow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        data = {}
        self.app = self.controller.submit_guardian_rejection(self.app, data)
        self.assertEqual(Youth.APPLICATION_STATUS_REJECTED, self.app.status)

    def test_unit_rejection(self):
        """ Test unit rejection flow """
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        data = {
            'unit_approval_user_id': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_rejection(self.app, data)
        self.assertEqual(Youth.APPLICATION_STATUS_REJECTED, self.app.status)

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

    def test_validation(self):
        """ Test object validation """
        if hasattr(self, 'obj'):
            self.assertTrue(self.validator.valid())


class TestUser(ModelTestCase):

    """ Tests User model """

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
    """ Tests Youth model """

    def setUp(self):
        """ Init """
        obj_data = {
            'duplicate_hash': 'foo',
            'units': [123, 456],
            'first_name': 'Test',
            'last_name': 'McTesterton',
            'date_of_birth': '2000-01-01',
        }
        self.factory = Youth.YouthFactory()
        self.obj = self.factory.construct(obj_data)
        self.persister = Youth.YouthPersister()
        self.validator = self.obj.get_validator()

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('yth', self.obj.uuid[0:3])

    def test_duplicate_search(self):
        """ Test duplicate check """
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

    """ Tests Volunteer model """

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

    """ Tests Guardian model """

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

    """ Tests District model """

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

    """ Tests Subdistrict model """

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

    """ Tests SponsoringOrganization model """

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

    """ Tests Unit model """

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


class TestYouthApplication(ModelTestCase):

    """ Tests Youth Application model """

    def setUp(self):
        """ Init """
        obj_data = {
            'status': Youth.APPLICATION_STATUS_COMPLETE,
            'unit_id': 'unt-123',
            'scoutnet_id': 123,
            'data': {}
        }
        self.factory = Youth.ApplicationFactory()
        self.obj = self.factory.construct(obj_data)
        self.persister = Youth.ApplicationPersister()
        self.validator = self.obj.get_validator()

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
        self.obj.status = Youth.APPLICATION_STATUS_UNIT_APPROVAL
        self.assertFalse(self.validator.valid())
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_unit_approval(self):
        """ Test unit approval validation """
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
        """ Test fee payment validation """
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
        """ Test ready for ScoutNet validation """
        self.obj.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET
        self.obj.guardian_approval_guardian_id = '123'
        self.obj.guardian_approval_signature = 'stuff'
        self.obj.guardian_approval_date = '2015-01-01'
        self.obj.unit_approval_user_id = '123'
        self.obj.unit_approval_signature = 'stuff'
        self.obj.unit_approval_date = '2015-01-01'
        self.assertTrue(self.validator.valid())

    def test_complete(self):
        """ Test complete status """
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
        """ Test reject status """
        self.obj.status = Youth.APPLICATION_STATUS_REJECTED
        self.assertFalse(self.validator.valid())
        self.obj.rejection_date = '2015-01-01'
        self.obj.rejection_reason = 'stuff'
        self.assertTrue(self.validator.valid())


class TestAdultApplications(ModelTestCase):

    """ Tests AdultApplications model """

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
    """ Tests CharterApplications model """

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


class TestUnitFactory(Unit.Factory):

    def load_by_uuid(self, uuid):
        unit_list = TestYouthApplicationController.get_test_unit_data()
        data = find_record_by_field('uuid', uuid, unit_list)
        return self.construct(data)


class TestYouthApplicationPersister(object):

    def get_by_status(self, status):
        app_list = TestYouthApplicationController.get_test_app_data()
        return [find_record_by_field('status', status, app_list)]


class TestYouthFactory(Youth.YouthFactory):

    def load_by_uuid(self, uuid):
        youth_list = TestYouthApplicationController.get_test_youth_data()
        data = find_record_by_field('uuid', uuid, youth_list)
        return self.construct(data)


class TestYouthPersister(object):

    def find_potential_duplicates(self, youth):
        youth_list = TestYouthApplicationController.get_test_youth_data()
        try:
            return [find_record_by_field('duplicate_hash', youth.get_record_hash(), youth_list)]
        except Base.RecordNotFoundException:
            return []


def find_record_by_field(field_name, field_value, data):
        record = None
        for item in data:
            if item[field_name] == field_value:
                record = item
                break
        if record:
            return record
        else:
            raise Base.RecordNotFoundException('Record matching {}="{}" not found'.format(field_name, field_value))


if __name__ == '__main__':
    unittest.main()
