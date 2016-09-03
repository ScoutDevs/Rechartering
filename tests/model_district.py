# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests models"""

import unittest

from models import District

from .model_base import ModelTestCase


class TestDistrict(ModelTestCase):

    """Tests District model"""

    def setUp(self):
        """Init"""
        obj_data = {
            'number': '5',
            'name': 'Provo Peak',
        }
        self._set_up(District, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('dst', self.obj.uuid[0:3])
        self.obj.number = '5'

        with self.assertRaises(Exception):
            self.obj.number = '4'


if __name__ == '__main__':
    unittest.main()
