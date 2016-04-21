# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests OrganizationController"""

import unittest

from controllers import ClientErrorException
from controllers import Organization
from models import Organization as OrganizationModel
from models import COUNCIL_ID
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
        user = FakeUserFactory().load_by_uuid('usr-ben')
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
        obj = self.controller.get('unt-51.spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID)
        self.assertEqual('unt-51.spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('Troop', obj.name)
        self.assertEqual('51', obj.number)
        self.assertEqual('spo-51.sbd-5-8.dst-5.cnl-'+COUNCIL_ID, obj.parent_uuid)

        with self.assertRaises(RecordNotFoundException):
            obj = self.controller.get('unt-NULL')
        with self.assertRaises(RecordNotFoundException):
            obj = self.controller.get('garbagio!')

    def test_get_sponsoring_org(self):
        """Test 'get' functionality"""
        obj = self.controller.get('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID)
        self.assertEqual('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('North Park 3rd Ward', obj.name)
        self.assertEqual('sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.parent_uuid)

    def test_get_district(self):
        """Test 'get' functionality"""
        obj = self.controller.get('dst-5.cnl-'+COUNCIL_ID)
        self.assertEqual('dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('Provo Peak', obj.name)
        self.assertEqual('5', obj.number)
        self.assertEqual('cnl-'+COUNCIL_ID, obj.parent_uuid)

    def test_get_subdistrict(self):
        """Test 'get' functionality"""
        obj = self.controller.get('sbd-5-9.dst-5.cnl-'+COUNCIL_ID)
        self.assertEqual('sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('Provo North Park Stake', obj.name)
        self.assertEqual('5-9', obj.number)
        self.assertEqual('dst-5.cnl-'+COUNCIL_ID, obj.parent_uuid)

    def test_search_unit(self):
        """Test 'search' functionality"""
        search_data = {
            'type': OrganizationModel.ORG_TYPE_UNIT,
            'number': '1455',
        }
        response = self.controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, response[0]['uuid'])

        search_data = {
            'parent_uuid': 'sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
        }
        response = self.controller.search(search_data)
        self.assertEqual(1, len(response))
        self.assertEqual('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, response[0]['uuid'])

    def test_set(self):
        """Test 'set' method"""
        orig_obj = self.controller.get('unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID)
        data = orig_obj.to_dict()
        data['name'] = 'Pack'
        obj = self.controller.set(data)
        self.assertEqual('unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('Pack', obj.name)

        orig_obj = self.controller.get('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID)
        data = orig_obj.to_dict()
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        orig_obj = self.controller.get('sbd-5-9.dst-5.cnl-'+COUNCIL_ID)
        data = orig_obj.to_dict()
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        orig_obj = self.controller.get('dst-5.cnl-'+COUNCIL_ID)
        data = orig_obj.to_dict()
        data['name'] = 'TEST NAME'
        obj = self.controller.set(data)
        self.assertEqual('dst-5.cnl-'+COUNCIL_ID, obj.uuid)
        self.assertEqual('TEST NAME', obj.name)

        with self.assertRaises(ClientErrorException):
            data = {
                'name': 'TEST NAME'
            }
            obj = self.controller.set(data)

    def test_update(self):
        """Test 'update' method"""
        data = {
            'uuid': 'unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID,
            'name': 'Pack',
        }
        obj = self.controller.update(data)
        self.assertEqual('unt-1455.spo-1455.sbd-5-9.dst-5.cnl-'+COUNCIL_ID, obj.uuid)
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
