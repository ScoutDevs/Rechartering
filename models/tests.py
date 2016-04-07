""" Tests models package """

import unittest
from . import Base
from . import User


class TestUser(unittest.TestCase):

    """ Tests User module """

    def test_uuid(self):
        """ Validate the UUID prefix """
        user = User.User({'username': 'foo', 'password': 'bar'})
        self.assertEquals('usr', user.uuid[0:3])

    def test_persistence(self):
        """ Test persistance of Users """
        user = User.User({'username': 'foo', 'password': 'bar'})
        factory = User.Factory()
        persister = User.Persister()

        persister.save(user)

        new_user = factory.load_by_uuid(user.uuid)
        self.assertEquals(new_user.uuid, user.uuid)

        persister.delete(user)
        with self.assertRaises(Base.RecordNotFoundException):
            factory.load_by_uuid(user.uuid)


if __name__ == '__main__':
    unittest.main()
