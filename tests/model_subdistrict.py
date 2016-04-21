# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests models"""

import unittest

from models import COUNCIL_ID
from models import Subdistrict

from . import FakeSubdistrictFactory
from .model_base import ModelTestCase


class TestSubdistrict(ModelTestCase):

    """Tests Subdistrict model"""

    def setUp(self):
        """Init"""
        obj_data = FakeSubdistrictFactory().load_by_uuid('sbd-5-9.dst-5.cnl-'+COUNCIL_ID).to_dict()
        self._set_up(Subdistrict, obj_data)

    def test_uuid(self):
        """Validate the UUID prefix"""
        self.assertEquals('sbd', self.obj.uuid[0:3])


if __name__ == '__main__':
    unittest.main()
