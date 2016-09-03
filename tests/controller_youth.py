# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests Youth.Controller"""

import unittest

from controllers import ClientErrorException
from controllers import Youth

from . import FakeGuardianFactory
from . import FakeUserFactory
from . import FakeYouthFactory


class TestYouthController(unittest.TestCase):
    """Test YouthController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-ken')
        youth_factory = FakeYouthFactory()

        self.controller = Youth.Controller(
            user,
            youth_factory,
        )

    def test_youth_lookup(self):
        """Test find_duplicate_youth method"""
        data = FakeYouthFactory().load_by_uuid('yth-TEST-1').to_dict()
        duplicates = self.controller.find_duplicate_youth(data)
        self.assertNotEqual(0, len(duplicates))

        data['first_name'] = 'yth-TEST-NULL'
        duplicates = self.controller.find_duplicate_youth(data)
        self.assertEqual(0, len(duplicates))

    def test_guardian_approval(self):
        """Test guardian approval"""
        youth = FakeYouthFactory().load_by_uuid('yth-TEST-1')
        data = {
            'guardian_approval_guardian_uuid': 'gdn-TEST-1',
            'guardian_approval_signature': 'SIG',
            'guardian_approval_date': '2016-05-01',
        }

        youth = self.controller.grant_guardian_approval(youth, data)
        self.assertEqual('gdn-TEST-1', youth.guardian_approval_guardian_uuid)
        self.assertEqual('SIG', youth.guardian_approval_signature)
        self.assertEqual('2016-05-01', youth.guardian_approval_date)

        guardian = FakeGuardianFactory().load_by_uuid('gdn-TEST-1')

        youth = self.controller.revoke_guardian_approval(guardian, youth)
        self.assertEqual('', youth.guardian_approval_guardian_uuid)
        self.assertEqual('', youth.guardian_approval_signature)
        self.assertEqual('', youth.guardian_approval_date)

    def test_no_access(self):
        """Test permissions"""
        pass
        # TO-DO: Uncomment this
        # with self.assertRaises(Security.InsufficientPermissionException):
        #   self.controller.get('yth-TEST-2')

    def test_get(self):
        """Test get method"""
        youth = self.controller.get('yth-TEST-1')
        self.assertEqual('Matthew', youth.first_name)

    def test_set(self):
        """Test set method"""
        data = {
            'first_name': 'Matt',
            'last_name': 'Reece',
            'date_of_birth': '2002-01-15',
            'duplicate_hash': 'b94302d98d30a3e48ea80c7f4432a6f30661869f0a95e0096f50e84edc0fc09b',
            'units': ['unt-TEST-1455'],
            'guardian_approval_guardian_uuid': 'gdn-TEST-123',
            'guardian_approval_signature': 'abcde',
        }
        youth = self.controller.set(data)
        self.assertNotEqual('', youth.uuid)
        self.assertEqual('Matt', youth.first_name)

    def test_update(self):
        """Test update method"""
        data = self.controller.get('yth-TEST-1').__dict__
        data['first_name'] = 'Matt'
        youth = self.controller.update(data)
        self.assertEqual('Matt', youth.first_name)

        with self.assertRaises(ClientErrorException):
            data['uuid'] = ''
            self.controller.update(data)

    def test_search(self):
        """Test 'search' method"""
        user = FakeUserFactory().load_by_uuid('usr-ben')
        youth_factory = FakeYouthFactory()
        controller = Youth.Controller(user, youth_factory)

        search_data = {
            'scoutnet_id': '123',
        }
        response = controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('yth-TEST-2', response[0]['uuid'])


if __name__ == '__main__':
    unittest.main()
