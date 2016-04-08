# pylint: disable=no-member
""" Tests models package """

import unittest
from . import Base
from . import User
from . import Youth


class ModelTestCase(unittest.TestCase):

    """ Parent for all model tests """

    def _test_persistence(self):
        """ Test persistance of object """
        self.persister.save(self.obj)

        new_obj = self.factory.load_by_uuid(self.obj.uuid)
        self.assertEquals(new_obj.uuid, self.obj.uuid)

        self.persister.delete(self.obj)
        with self.assertRaises(Base.RecordNotFoundException):
            self.factory.load_by_uuid(self.obj.uuid)


class TestUser(ModelTestCase):

    """ Tests User module """

    def setUp(self):
        """ Init """
        obj_data = {
            'username': 'foo',
            'password': 'bar',
        }
        self.obj = User.User(obj_data)
        self.factory = User.Factory()
        self.persister = User.Persister()

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('usr', self.obj.uuid[0:3])

    def test_persistence(self):
        """ Test persistence in parent """
        self._test_persistence()


class TestYouth(ModelTestCase):

    """ Tests Youth module """

    def setUp(self):
        """ Init """
        obj_data = {
            'duplicate_hash': 'foo',
            'units': [123, 456],
        }
        self.obj = Youth.Youth(obj_data)
        self.factory = Youth.Factory()
        self.persister = Youth.Persister()

    def test_uuid(self):
        """ Validate the UUID prefix """
        self.assertEquals('yth', self.obj.uuid[0:3])

    def test_persistence(self):
        """ Test persistence in parent """
        self._test_persistence()


if __name__ == '__main__':
    unittest.main()
