# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests Session model"""

import datetime
import unittest

from models import Session

from .model_base import ModelTestCase


class TestSession(ModelTestCase):

    """Tests Session model"""

    def setUp(self):
        """Init"""

    def test_init(self):
        """Validate the init"""
        obj = Session.Session()
        self.assertEquals('ses', obj.uuid[0:3])

        delta = obj.expires - datetime.datetime.now()
        self.assertTrue(delta.total_seconds() > Session.Session.EXPIRES_AFTER_SECONDS - 1)
        self.assertTrue(delta.total_seconds() < Session.Session.EXPIRES_AFTER_SECONDS + 1)

    def test_data(self):
        """Test session data"""
        obj = Session.Session()
        obj.set('test', 'stuff')
        self.assertEqual('stuff', obj.get('test'))


if __name__ == '__main__':
    unittest.main()
