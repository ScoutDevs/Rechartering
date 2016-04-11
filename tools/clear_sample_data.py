#!/usr/bin/python

# pylint: disable=no-member
""" clears sample data to prime the pump """

from . import User
from . import Youth
from . import Volunteers
from . import Guardians
from . import Districts
from . import Subdistricts
from . import SponsoringOrganizations
from . import Units
from . import YouthApplications
from . import AdultApplications
from . import CharterApplications
from . import sample_data


def clear_objects(module, source_data):
    """ Clear the objects from persistence """
    factory = module.Factory()
    persister = module.Persister()

    for data in source_data:
        obj = factory.construct(data)
        persister.delete(obj)


def main():
    """ Clear all sample data """
    clear_objects(User, sample_data.USER_DATA)
    clear_objects(Youth, sample_data.YOUTH_DATA)
    clear_objects(Volunteers, sample_data.VOLUNTEERS_DATA)
    clear_objects(Guardians, sample_data.GUARDIANS_DATA)
    clear_objects(Districts, sample_data.DISTRICTS_DATA)
    clear_objects(Subdistricts, sample_data.SUBDISTRICTS_DATA)
    clear_objects(SponsoringOrganizations, sample_data.SPONSORING_ORGANIZATIONS_DATA)
    clear_objects(Units, sample_data.UNITS_DATA)
    clear_objects(YouthApplications, sample_data.YOUTH_APPLICATIONS_DATA)
    clear_objects(AdultApplications, sample_data.ADULT_APPLICATIONS_DATA)
    clear_objects(CharterApplications, sample_data.CHARTER_APPLICATIONS_DATA)

if __name__ == '__main__':
    main()
