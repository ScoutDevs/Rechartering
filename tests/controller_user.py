# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests User.Controller"""

import unittest

from controllers import ClientErrorException
from controllers import User
from models import AuthenticationFailureException

from . import FakeUserFactory


class TestUserController(unittest.TestCase):
    """Test UserController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-ken')
        user_factory = FakeUserFactory()

        self.controller = User.Controller(
            user,
            user_factory,
        )

    def test_no_access(self):
        """Test permissions"""
        pass
        # TO-DO: Uncomment this
        # with self.assertRaises(Security.InsufficientPermissionException):
        #   self.controller.get('gdn-TEST-2')

    def test_get(self):
        """Test get method"""
        user = self.controller.get('usr-ben')
        self.assertEqual('Ben', user.first_name)

    def test_set(self):
        """Test set method"""
        data = {
            'username': 'ben',
            'first_name': 'Ben',
            'last_name': 'Reece',
            'password': 'foo',
        }
        user = self.controller.set(data)
        self.assertNotEqual('', user.uuid)
        self.assertEqual('Ben', user.first_name)

    def test_update(self):
        """Test update method"""
        data = self.controller.get('usr-ben').__dict__
        data['first_name'] = 'Matt'
        user = self.controller.update(data)
        self.assertEqual('Matt', user.first_name)

        with self.assertRaises(ClientErrorException):
            data['uuid'] = ''
            self.controller.update(data)

    def test_search(self):
        """Test 'search' method"""
        user = FakeUserFactory().load_by_uuid('usr-ben')
        user_factory = FakeUserFactory()
        controller = User.Controller(user, user_factory)

        search_data = {
            'last_name': 'Reece',
        }
        response = controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('usr-ben', response[0]['uuid'])

    def test_login(self):
        """Test 'log_in' method"""
        controller = User.Controller(None, FakeUserFactory())

        user = controller.log_in('ben', 'ben')
        self.assertEqual('usr-ben', user.uuid)

        with self.assertRaises(AuthenticationFailureException):
            controller.log_in('fred', 'flintstone')

if __name__ == '__main__':
    unittest.main()
