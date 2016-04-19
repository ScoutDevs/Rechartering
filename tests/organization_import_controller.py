# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests OrganizationController"""

import os
import unittest

from controllers import OrganizationImport

from . import FakeDistrictFactory
from . import FakeSponsoringOrganizationFactory
from . import FakeSubdistrictFactory
from . import FakeUserFactory


class TestOrganizationImportController(unittest.TestCase):
    """Test OrganizationImportController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-TEST-ben')
        district_factory = FakeDistrictFactory()
        subdistrict_factory = FakeSubdistrictFactory()
        sponsoringorganization_factory = FakeSponsoringOrganizationFactory()
        self.controller = OrganizationImport.Controller(
            user,
            district_factory,
            subdistrict_factory,
            sponsoringorganization_factory,
        )

    def test_process_file(self):
        """Tests the process_file method"""
        filename = os.path.join(os.path.dirname(__file__), 'data/orgs.tsv')
        data = self.controller.process_file(filename)
        self.assertEqual(3, len(data['districts']))
        self.assertEqual(6, len(data['subdistricts']))
        self.assertEqual(8, len(data['sponsoring_organizations']))
        self.assertEqual('dst-TEST-provopeak', data['districts']['5'].uuid)
        self.assertEqual('sbd-TEST-nps', data['subdistricts']['5-9'].uuid)
        self.assertEqual('spo-TEST-np3', data['sponsoring_organizations']['1455'].uuid)


if __name__ == '__main__':
    unittest.main()
