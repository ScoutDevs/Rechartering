#!/usr/bin/python
"""Creates sample data to prime the pump"""

from . import User

USER_DATA = [
    {
        'uuid': 'usr-1',
        'username': 'ben',
        'password': User.User.get_password_hash('password'),
        'roles': {},
        'positions': [],
        'guardians': [],
    },
    {
        'uuid': 'usr-2',
        'username': 'ken',
        'password': User.User.get_password_hash('password'),
        'roles': {},
        'positions': [],
        'guardians': [],
    },
    {
        'uuid': 'usr-3',
        'username': 'callie',
        'password': User.User.get_password_hash('password'),
        'roles': {},
        'positions': [],
        'guardians': [],
    },
]

YOUTH_DATA = [
    {
        'uuid': 'yth-1',
        'units': [],
        'scoutnet_id': 0,
        'application_uuid': 0,
        'guardians': [],
        'first_name': 'Matthew',
        'last_name': 'Reece',
        'date_of_birth': '2002-01-15',
    },
    {
        'uuid': 'yth-2',
        'units': [],
        'scoutnet_id': 0,
        'application_uuid': 0,
        'guardians': [],
        'first_name': 'Jacob',
        'last_name': 'Reece',
        'date_of_birth': '2005-12-22',
    },
]

VOLUNTEERS_DATA = [
    {
        'uuid': 'vol-1',
        'unit_uuid': 'unt-1',
        'ssn': '123-45-678',
        'first_name': 'Ben',
        'last_name': 'Reece',
        'scoutnet_id': 0,
        'application_uuid': 0,
        'ypt_completion_date': '2015-01-01',
    },
    {
        'uuid': 'vol-2',
        'unit_uuid': 'unt-2',
        'ssn': '234-56-789',
        'first_name': 'Cami',
        'last_name': 'Reece',
        'scoutnet_id': 0,
        'application_uuid': 0,
        'ypt_completion_date': '2015-01-01',
    },
]

GUARDIANS_DATA = [
    {
        'uuid': 'gdn-1',
        'youth': {'yth-1', 'yth-2'},
        'first_name': 'Ben',
        'last_name': 'Reece',
    },
    {
        'uuid': 'gdn-2',
        'youth': {'yth-1', 'yth-2'},
        'first_name': 'Cami',
        'last_name': 'Reece',
    },
]

DISTRICTS_DATA = [
    {
        'uuid': 'dst-1',
        'number': '05',
        'name': 'Provo Peak',
    },
    {
        'uuid': 'dst-2',
        'number': '06',
        'name': 'Some other district',
    },
]

SUBDISTRICTS_DATA = [
    {
        'uuid': 'sbd-1',
        'district_uuid': 'dst-1',
        'number': '05-9',
        'name': 'Provo North Park Stake',
    },
    {
        'uuid': 'sbd-2',
        'district_uuid': 'dst-1',
        'number': '05-11',
        'name': 'Provo South Stake',
    },
    {
        'uuid': 'sbd-3',
        'district_uuid': 'dst-2',
        'number': '06-1',
        'name': 'Some random subdistrict',
    },
]

SPONSORING_ORGANIZATIONS_DATA = [
    {
        'uuid': 'spo-1',
        'subdistrict_uuid': 'sbd-1',
        'name': 'North Park 3rd Ward',
    },
    {
        'uuid': 'spo-2',
        'subdistrict_uuid': 'sbd-1',
        'name': 'North Park 2nd Ward',
    },
    {
        'uuid': 'spo-3',
        'subdistrict_uuid': 'sbd-2',
        'name': 'Provo 6th Ward',
    },
]

UNITS_DATA = [
    {
        'uuid': 'unt-1',
        'sponsoring_organization_uuid': 'spo-1',
        'type': 'Troop',
        'number': 1455,
    },
    {
        'uuid': 'unt-2',
        'sponsoring_organization_uuid': 'spo-1',
        'type': 'Team',
        'number': 1455,
    },
    {
        'uuid': 'unt-3',
        'sponsoring_organization_uuid': 'spo-1',
        'type': 'Crew',
        'number': 1455,
    },
    {
        'uuid': 'unt-4',
        'sponsoring_organization_uuid': 'spo-1',
        'type': 'Pack',
        'number': 1455,
    },
    {
        'uuid': 'unt-5',
        'sponsoring_organization_uuid': 'spo-2',
        'type': 'Troop',
        'number': 742,
    },
]

YOUTH_APPLICATIONS_DATA = [
]

ADULT_APPLICATIONS_DATA = []

CHARTER_APPLICATIONS_DATA = []
