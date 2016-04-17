# pylint: disable=no-member,attribute-defined-outside-init,import-error
""" General functionality for use across tests """

from models import Base
from models import Unit
from models import Youth


class FakeUnitFactory(Unit.Factory):  # pylint: disable=too-few-public-methods,no-init
    """ Fake class for testing """

    def load_by_uuid(self, uuid):
        """ Fake method for testing """
        unit_list = get_test_unit_data()
        data = find_record_by_field('uuid', uuid, unit_list)
        return self.construct(data)


class FakeYouthApplicationPersister(object):  # pylint: disable=too-few-public-methods
    """ Fake class for testing """

    @staticmethod
    def get_by_status(status):
        """ Fake method for testing """
        app_list = get_test_app_data()
        return [find_record_by_field('status', status, app_list)]


class FakeYouthFactory(Youth.YouthFactory):  # pylint: disable=too-few-public-methods,no-init
    """ Fake class for testing """

    def load_by_uuid(self, uuid):
        """ Fake method for testing """
        youth_list = get_test_youth_data()
        data = find_record_by_field('uuid', uuid, youth_list)
        return self.construct(data)


class FakeYouthPersister(object):  # pylint: disable=too-few-public-methods
    """ Fake class for testing """

    @staticmethod
    def find_potential_duplicates(youth):
        """ Fake method for testing """
        youth_list = get_test_youth_data()
        try:
            return [find_record_by_field('duplicate_hash', youth.get_record_hash(), youth_list)]
        except Base.RecordNotFoundException:
            return []


def find_record_by_field(field_name, field_value, data):
    """ Finds a test data record by the specified field & value """
    record = None
    for item in data:
        if item[field_name] == field_value:
            record = item
            break
    if record:
        return record
    else:
        raise Base.RecordNotFoundException('Record matching {}="{}" not found'.format(field_name, field_value))


def get_test_user_data():
    """ Test User data """
    return [
        {
            'username': 'ben',
            'password': 'ben',
            'guardian_id': 'grd-TEST-1',
            'roles': {
                'Council.Admin': [],
            },
            'positions': [
            ]
        },
    ]


def get_test_app_data():
    """ Test Youth Application data """
    return [
        {
            'unit_id': 'unt-TEST-123',
            'scoutnet_id': 123,
            'status': Youth.APPLICATION_STATUS_CREATED,
            'first_name': 'Ben',
            'last_name': 'Reece',
            'date_of_birth': '1970-01-01',
        },
    ]


def get_test_youth_data():
    """ test Youths data """
    return [
        {
            'uuid': 'yth-TEST-1',
            'first_name': 'Matthew',
            'last_name': 'Reece',
            'date_of_birth': '2002-01-15',
            'duplicate_hash': 'b94302d98d30a3e48ea80c7f4432a6f30661869f0a95e0096f50e84edc0fc09b',
            'units': ['unt-TEST-123'],
            'guardian_approval_guardian_id': 'grd-TEST-123',
            'guardian_approval_signature': 'abcde',
        },
    ]


def get_test_unit_data():
    """ Test Unit data """
    return [
        {
            'uuid': 'unt-TEST-51',
            'sponsoring_organization_id': 'spo-TEST-51',
            'type': Unit.TYPE_TROOP,
            'number': 51,
            'lds_unit': False,
        },
        {
            'uuid': 'unt-TEST-123',
            'sponsoring_organization_id': 'spo-TEST-123',
            'type': Unit.TYPE_TROOP,
            'number': 1455,
            'lds_unit': True,
        },
    ]
