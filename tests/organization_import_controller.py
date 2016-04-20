# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests OrganizationController"""

import os
import unittest

from controllers import ClientErrorException
from controllers import OrganizationImport

from . import FakeDistrictFactory
from . import FakeSponsoringOrganizationFactory
from . import FakeSubdistrictFactory


class TestOrganizationImportController(unittest.TestCase):
    """Test OrganizationImportController"""

    def setUp(self):
        district_factory = FakeDistrictFactory()
        subdistrict_factory = FakeSubdistrictFactory()
        sponsoringorganization_factory = FakeSponsoringOrganizationFactory()
        self.controller = OrganizationImport.Controller(
            district_factory,
            subdistrict_factory,
            sponsoringorganization_factory,
        )

    def test_process_file(self):
        """Tests the process_file method"""
        filename = os.path.join(os.path.dirname(__file__), 'data/orgs.tsv')
        districts = {}
        subdistricts = {}
        sporgs = {}

        for data in self.controller.process_file(filename):
            (district, subdistrict, sporg) = self.controller.process_record(data)
            districts[district.number] = district
            subdistricts[subdistrict.number] = subdistrict
            sporgs[sporg.number] = sporg

        self.assertEqual(3, len(districts))
        self.assertEqual(6, len(subdistricts))
        self.assertEqual(8, len(sporgs))
        self.assertEqual('dst-TEST-provopeak', districts['5'].uuid)
        self.assertEqual('sbd-TEST-nps', subdistricts['5-9'].uuid)
        self.assertEqual('spo-TEST-np3', sporgs['1455'].uuid)

        with self.assertRaises(ClientErrorException):
            filename = os.path.join(os.path.dirname(__file__), 'data/orgs_bad.tsv')
            for data in self.controller.process_file(filename):
                pass


if __name__ == '__main__':
    unittest.main()
