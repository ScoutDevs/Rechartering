# pylint: disable=no-member,attribute-defined-outside-init
""" Tests controllers package """

import unittest
import shortuuid
from . import YouthApplication
from models import Units
from models import YouthApplications
from models import Youth

ENVIRONMENT = 'dev'  # 'dev-persist' for persistence tests


class TestYouthApplication(unittest.TestCase):
    """ Test YouthApplication controller """

    def setUp(self):
        app_data = self.__class__.get_test_app_data()
        self.app = YouthApplications.Factory().construct(app_data)
        self.controller = YouthApplication.YouthApplication()

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
        """ Test Units data """
        return [
            {
                'uuid': 'unt-TEST-51',
                'sponsoring_organization_id': 'spo-TEST-51',
                'type': Units.TYPE_TROOP,
                'number': 51,
                'lds_unit': False,
            },
            {
                'uuid': 'unt-TEST-123',
                'sponsoring_organization_id': 'spo-TEST-123',
                'type': Units.TYPE_TROOP,
                'number': 1455,
                'lds_unit': True,
            },
        ]

    def test_youth_lookup(self):
        """ Test look_up_youth method """
        if ENVIRONMENT == 'dev-persist':
            data = self.__class__.get_test_youth_data()
            duplicates = self.controller.look_up_youth(data)
            self.assertNotEqual(0, len(duplicates))

            data['first_name'] = shortuuid.uuid()
            duplicates = self.controller.look_up_youth(data)
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
        # TODO: implement this
        pass

    def test_unit_rejection(self):
        """ Test unit rejection flow """
        # TODO: implement this
        pass

    def test_invalid_workflows(self):
        """ Test invalid workflow exceptions """
        # TODO: implement this
        pass


def init_data():
    """ Create records in DB for testing """
    if ENVIRONMENT == 'dev-persist':
        data = TestYouthApplication.get_test_youth_data()
        youth = Youth.Factory().construct(data)
        Youth.Persister().save(youth)

        units = TestYouthApplication.get_test_unit_data()
        for unit_data in units:
            unit = Units.Factory().construct(unit_data)
            Units.Persister().save(unit)


def clear_data():
    """ Clean up test data """
    if ENVIRONMENT == 'dev-persist':
        data = TestYouthApplication.get_test_youth_data()
        youth = Youth.Factory().construct(data)
        Youth.Persister().delete(youth)

        units = TestYouthApplication.get_test_unit_data()
        for unit_data in units:
            unit = Units.Factory().construct(unit_data)
            Units.Persister().delete(unit)


if __name__ == '__main__':
    init_data()
    unittest.main()
    clear_data()
