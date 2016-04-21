# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests Youth.Controller"""

import unittest

from controllers import Youth

from . import FakeUserFactory
from . import FakeYouthFactory


class TestYouthApplicationController(unittest.TestCase):
    """Test YouthApplicationController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-ben')
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


if __name__ == '__main__':
    unittest.main()
