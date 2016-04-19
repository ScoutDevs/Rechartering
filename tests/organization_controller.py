# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests OrganizationController"""

import unittest
from . import FakeUnitFactory
from . import FakeDistrictFactory
from . import FakeSubdistrictFactory
from . import FakeSponsoringOrganizationFactory
from . import FakeOrganizationPersister
from controllers import Organization
from models import Organization as OrganizationModel
from models import RecordNotFoundException


class TestOrganizationController(unittest.TestCase):
    """Test OrganizationController"""

    def setUp(self):
        district_factory = FakeDistrictFactory()
        subdistrict_factory = FakeSubdistrictFactory()
        sponsoringorganization_factory = FakeSponsoringOrganizationFactory()
        unit_factory = FakeUnitFactory()
        organization_persister = FakeOrganizationPersister()
        self.controller = Organization.Controller(
            district_factory,
            subdistrict_factory,
            sponsoringorganization_factory,
            unit_factory,
            organization_persister,
        )

    def test_get_unit(self):
        """Test 'get' functionality"""
        obj = self.controller.get('unt-TEST-51')
        self.assertEqual('unt-TEST-51', obj.uuid)
        self.assertEqual('Troop', obj.unit_type)
        self.assertEqual('51', obj.number)
        self.assertEqual('spo-TEST-provocity', obj.parent_uuid)

        with self.assertRaises(RecordNotFoundException):
            obj = self.controller.get('unt-NULL')
        with self.assertRaises(RecordNotFoundException):
            obj = self.controller.get('garbagio!')

    def test_get_sponsoring_org(self):
        """Test 'get' functionality"""
        obj = self.controller.get('spo-TEST-np3')
        self.assertEqual('spo-TEST-np3', obj.uuid)
        self.assertEqual('North Park 3rd Ward', obj.name)
        self.assertEqual('sbd-TEST-nps', obj.parent_uuid)

    def test_get_district(self):
        """Test 'get' functionality"""
        obj = self.controller.get('dst-TEST-provopeak')
        self.assertEqual('dst-TEST-provopeak', obj.uuid)
        self.assertEqual('Provo Peak', obj.name)
        self.assertEqual('5', obj.number)
        self.assertEqual('COUNCIL', obj.parent_uuid)

    def test_get_subdistrict(self):
        """Test 'get' functionality"""
        obj = self.controller.get('sbd-TEST-nps')
        self.assertEqual('sbd-TEST-nps', obj.uuid)
        self.assertEqual('Provo North Park Stake', obj.name)
        self.assertEqual('5-9', obj.number)
        self.assertEqual('dst-TEST-provopeak', obj.parent_uuid)

    def test_search_unit(self):
        """Test 'search' functionality"""
        search_data = {
            'type': OrganizationModel.ORG_TYPE_UNIT,
            'number': '1455',
        }
        response = self.controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('unt-TEST-1455', response[0]['uuid'])

        search_data = {
            'parent_uuid': 'sbd-TEST-nps',
        }
        response = self.controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('spo-TEST-np3', response[0]['uuid'])


if __name__ == '__main__':
    unittest.main()
