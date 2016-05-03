# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests Volunteer.Controller"""

import unittest

from controllers import ClientErrorException
from controllers import Volunteer

from . import FakeUserFactory
from . import FakeVolunteerFactory


class TestVolunteerController(unittest.TestCase):
    """Test VolunteerController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-ken')
        volunteer_factory = FakeVolunteerFactory()

        self.controller = Volunteer.Controller(
            user,
            volunteer_factory,
        )

    def test_no_access(self):
        """Test permissions"""
        pass
        # TO-DO: Uncomment this
        # with self.assertRaises(Security.InsufficientPermissionException):
        #   self.controller.get('gdn-TEST-2')

    def test_get(self):
        """Test get method"""
        volunteer = self.controller.get('vol-TEST-1')
        self.assertEqual('Ben', volunteer.first_name)

    def test_set(self):
        """Test set method"""
        data = {
            'uuid': 'vol-TEST-1',
            'user_uuid': 'usr-ben',
            'first_name': 'Ben',
            'last_name': 'Reece',
            'unit_uuid': 'unt-TEST-1455',
            'ypt_completion_date': '2016-01-01',
            'ssn': '123-45-6789',
        }
        volunteer = self.controller.set(data)
        self.assertNotEqual('', volunteer.uuid)
        self.assertEqual('Ben', volunteer.first_name)

    def test_update(self):
        """Test update method"""
        data = self.controller.get('vol-TEST-1').__dict__
        data['first_name'] = 'Matt'
        volunteer = self.controller.update(data)
        self.assertEqual('Matt', volunteer.first_name)

        with self.assertRaises(ClientErrorException):
            data['uuid'] = ''
            self.controller.update(data)

    def test_search(self):
        """Test 'search' method"""
        user = FakeUserFactory().load_by_uuid('usr-ben')
        volunteer_factory = FakeVolunteerFactory()
        controller = Volunteer.Controller(user, volunteer_factory)

        search_data = {
            'last_name': 'Reece',
        }
        response = controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('vol-TEST-1', response[0]['uuid'])


if __name__ == '__main__':
    unittest.main()
