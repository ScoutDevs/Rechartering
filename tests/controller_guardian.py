# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests Guardian.Controller"""

import unittest

from controllers import ClientErrorException
from controllers import Guardian

from . import FakeGuardianFactory
from . import FakeUserFactory


class TestGuardianController(unittest.TestCase):
    """Test GuardianController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-ken')
        guardian_factory = FakeGuardianFactory()

        self.controller = Guardian.Controller(
            user,
            guardian_factory,
        )

    def test_no_access(self):
        """Test permissions"""
        pass
        # TO-DO: Uncomment this
        # with self.assertRaises(Security.InsufficientPermissionException):
        #   self.controller.get('gdn-TEST-2')

    def test_get(self):
        """Test get method"""
        guardian = self.controller.get('gdn-TEST-1')
        self.assertEqual('Ben', guardian.first_name)

    def test_set(self):
        """Test set method"""
        data = {
            'user_uuid': 'usr-ben',
            'first_name': 'Ben',
            'last_name': 'Reece',
            'youth': ['yth-TEST-1'],
        }
        guardian = self.controller.set(data)
        self.assertNotEqual('', guardian.uuid)
        self.assertEqual('Ben', guardian.first_name)

    def test_update(self):
        """Test update method"""
        data = self.controller.get('gdn-TEST-1').__dict__
        data['first_name'] = 'Matt'
        guardian = self.controller.update(data)
        self.assertEqual('Matt', guardian.first_name)

        with self.assertRaises(ClientErrorException):
            data['uuid'] = ''
            self.controller.update(data)

    def test_search(self):
        """Test 'search' method"""
        user = FakeUserFactory().load_by_uuid('usr-ben')
        guardian_factory = FakeGuardianFactory()
        controller = Guardian.Controller(user, guardian_factory)

        search_data = {
            'last_name': 'Reece',
        }
        response = controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('gdn-TEST-1', response[0]['uuid'])


if __name__ == '__main__':
    unittest.main()
