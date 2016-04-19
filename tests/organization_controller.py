# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests OrganizationController"""

import unittest

from controllers import ClientErrorException
from controllers import Organization
from models import Organization as OrganizationModel
from models import RecordNotFoundException

from . import FakeDistrictFactory
from . import FakeOrganizationPersister
from . import FakeSponsoringOrganizationFactory
from . import FakeSubdistrictFactory
from . import FakeUnitFactory
from . import FakeUserFactory


class TestOrganizationController(unittest.TestCase):
    """Test OrganizationController"""

    def setUp(self):
        user = FakeUserFactory().load_by_uuid('usr-TEST-ben')
        district_factory = FakeDistrictFactory()
        subdistrict_factory = FakeSubdistrictFactory()
        sponsoringorganization_factory = FakeSponsoringOrganizationFactory()
        unit_factory = FakeUnitFactory()
        organization_persister = FakeOrganizationPersister()
        self.controller = Organization.Controller(
            user,
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
        self.assertEqual('Troop', obj.name)
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

    def test_set(self):
        """Test 'set' method"""
        orig_obj = self.controller.get('unt-TEST-1455')
        data = orig_obj.__dict__
        data['name'] = 'Pack'
        obj = self.controller.set(data)
        self.assertEqual('unt-TEST-1455', obj.uuid)
        self.assertEqual('Pack', obj.name)

        orig_obj = self.controller.get('spo-TEST-np3')
        data = orig_obj.__dict__
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('spo-TEST-np3', obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        orig_obj = self.controller.get('sbd-TEST-nps')
        data = orig_obj.__dict__
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('sbd-TEST-nps', obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        orig_obj = self.controller.get('dst-TEST-provopeak')
        data = orig_obj.__dict__
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('dst-TEST-provopeak', obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        with self.assertRaises(ClientErrorException):
            data = {
                'name': 'TEST NAME'
            }
            obj = self.controller.set(data)

    def test_update(self):
        """Test 'update' method"""
        data = {
            'uuid': 'unt-TEST-1455',
            'name': 'Pack',
        }
        obj = self.controller.update(data)
        self.assertEqual('unt-TEST-1455', obj.uuid)
        self.assertEqual('Pack', obj.name)
        self.assertEqual('1455', obj.number)

        with self.assertRaises(RecordNotFoundException):
            data['uuid'] = 'TEST-NULL'
            obj = self.controller.update(data)

        with self.assertRaises(ClientErrorException):
            del data['uuid']
            obj = self.controller.update(data)


if __name__ == '__main__':
    unittest.main()
