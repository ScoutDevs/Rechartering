#!/usr/bin/python

# pylint: disable=no-member
"""clears sample data to prime the pump"""

from . import AdultApplications
from . import CharterApplications
from . import District
from . import Guardian
from . import SponsoringOrganization
from . import Subdistrict
from . import Unit
from . import User
from . import Volunteer
from . import Youth
from . import YouthApplications
from . import sample_data


def clear_objects(module, source_data):
    """Clear the objects from persistence"""
    factory = module.Factory()
    persister = module.Persister()

    for data in source_data:
        obj = factory.construct(data)
        persister.delete(obj)


def main():
    """Clear all sample data"""
    clear_objects(User, sample_data.USER_DATA)
    clear_objects(Youth, sample_data.YOUTH_DATA)
    clear_objects(Volunteer, sample_data.VOLUNTEERS_DATA)
    clear_objects(Guardian, sample_data.GUARDIANS_DATA)
    clear_objects(District, sample_data.DISTRICTS_DATA)
    clear_objects(Subdistrict, sample_data.SUBDISTRICTS_DATA)
    clear_objects(SponsoringOrganization, sample_data.SPONSORING_ORGANIZATIONS_DATA)
    clear_objects(Unit, sample_data.UNITS_DATA)
    clear_objects(YouthApplications, sample_data.YOUTH_APPLICATIONS_DATA)
    clear_objects(AdultApplications, sample_data.ADULT_APPLICATIONS_DATA)
    clear_objects(CharterApplications, sample_data.CHARTER_APPLICATIONS_DATA)

if __name__ == '__main__':
    main()
