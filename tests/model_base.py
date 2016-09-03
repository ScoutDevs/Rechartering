# pylint: disable=no-member,attribute-defined-outside-init,import-error
"""Tests models"""

import unittest


class ModelTestCase(unittest.TestCase):

    """Parent for all model tests"""

    def _set_up(self, module, obj_data):
        """Set up for all children"""
        self.factory = module.Factory()
        self.obj = self.factory.construct(obj_data)
        self.validator = self.obj.get_validator()

    def test_validation(self):
        """Test object validation"""
        if hasattr(self, 'obj'):
            self.assertTrue(self.validator.valid())
