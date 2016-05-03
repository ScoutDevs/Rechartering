# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests YouthApplicationController"""

import unittest

from controllers import InvalidActionException
from controllers import YouthApplication
from models import COUNCIL_ID
from models import Youth

from . import FakeUnitFactory
from . import FakeUserFactory
from . import FakeYouthApplicationFactory
from . import FakeYouthFactory


class TestYouthApplicationController(unittest.TestCase):
    """Test YouthApplicationController"""

    def setUp(self):
        self.app = FakeYouthApplicationFactory().load_by_uuid('yap-TEST-1')

        user = FakeUserFactory().load_by_uuid('usr-ben')
        application_factory = FakeYouthApplicationFactory()
        unit_factory = FakeUnitFactory()
        youth_factory = FakeYouthFactory()
        self.controller = YouthApplication.Controller(
            user,
            application_factory,
            unit_factory,
            youth_factory,
        )

    def test_status_search(self):
        """Test get_applications_by_status()"""
        app_list = self.controller.get_applications_by_status(Youth.APPLICATION_STATUS_CREATED)
        self.assertNotEqual(0, len(app_list))

    def test_new_youth(self):
        """Test new youth workflow"""
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_uuid': 'gdn-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        (self.app, _) = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        unit_approval = {
            'unit_approval_user_uuid': 'usr-ben',
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
        """Test workflow when the guardian approval is on file"""
        data = FakeYouthFactory().load_by_uuid('yth-TEST-1')
        self.app.youth_uuid = data.uuid
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

    def test_non_lds_flow(self):
        """Test flow with non-LDS unit"""
        self.app.unit_uuid = 'unt-51.spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_uuid': 'gdn-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        (self.app, _) = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        unit_approval = {
            'unit_approval_user_uuid': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_approval(self.app, unit_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_FEE_PENDING, self.app.status)

        fee_data = {
            'fee_payment_user_uuid': 'usr-TEST-123',
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
        """Test guardian rejection flow"""
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        data = {}
        self.app = self.controller.submit_guardian_rejection(self.app, data)
        self.assertEqual(Youth.APPLICATION_STATUS_REJECTED, self.app.status)

    def test_unit_rejection(self):
        """Test unit rejection flow"""
        self.app = self.controller.submit_application(self.app)
        self.assertEqual(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL, self.app.status)

        guardian_approval = {
            'guardian_approval_guardian_uuid': 'gdn-TEST-123',
            'guardian_approval_signature': 'abcd',
        }
        (self.app, _) = self.controller.submit_guardian_approval(self.app, guardian_approval)
        self.assertEqual(Youth.APPLICATION_STATUS_UNIT_APPROVAL, self.app.status)

        data = {
            'unit_approval_user_uuid': 'usr-TEST-123',
            'unit_approval_signature': 'abcd',
        }
        self.app = self.controller.submit_unit_rejection(self.app, data)
        self.assertEqual(Youth.APPLICATION_STATUS_REJECTED, self.app.status)

    def test_invalid_workflows(self):
        """Test invalid workflow exceptions"""
        with self.assertRaises(InvalidActionException):
            guardian_approval = {
                'guardian_approval_guardian_uuid': 'gdn-TEST-123',
                'guardian_approval_signature': 'abcd',
            }
            self.controller.submit_guardian_approval(self.app, guardian_approval)

        with self.assertRaises(InvalidActionException):
            unit_approval = {
                'unit_approval_user_uuid': 'usr-TEST-123',
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


if __name__ == '__main__':
    unittest.main()
