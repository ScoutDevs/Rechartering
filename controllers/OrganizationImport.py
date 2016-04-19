# pylint: disable=import-error
"""Organization Import Controller"""

import csv
import StringIO
from models import District
from models import SponsoringOrganization
from models import Subdistrict


class Controller(object):
    """Organization Import Controller

    'Organization' in this case includes districts, subdistricts, and
    sponsoring organizations.

    The Council keeps a list of the various organizations in spreadsheet.
    This will take a TSV (tab-separated values) file, process it, and
    give back a dict with all the objects with relationships defined.
    """

    def __init__(self,
                 user,
                 district_factory=District.Factory(),
                 subdistrict_factory=Subdistrict.Factory(),
                 sponsoringorganization_factory=SponsoringOrganization.Factory()):
        self.user = user
        self.district_factory = district_factory
        self.subdistrict_factory = subdistrict_factory
        self.sponsoringorganization_factory = sponsoringorganization_factory

    def process_s3_object(self, s3_object):
        """Process the data as it comes in from S3

        Args:
            s3_object: boto3 s3_object object
        Returns:
            dict
        """
        data = s3_object['Body'].read()
        data_file = StringIO.StringIO(data)
        return self._process_file(data_file)

    def process_file(self, filename):
        """Process the data as it comes in from a local file

        Args:
            filename: name of local file
        Returns:
            dict
        """
        with open(filename) as tsv_file:
            return self._process_file(tsv_file)

    def _process_file(self, data_file):
        """Processes the data file provided by the council

        The council can drop off a data file into an S3 bucket for processing.
        This action kicks off a Lambda function which calls this method.  The
        file the council provides is a flat file with the following fields:
            District No
            District Name
            Sub District #
            Stake/Sub District Name
            Unit No
            Ward/Sponsoring Org
            New Number
            Date
            Processor Name

        Args:
            data_file: file containing data
        Returns:
            dict
        """
        reader = csv.DictReader(data_file, dialect=csv.excel_tab)
        districts = {}
        subdistricts = {}
        sponsoring_organizations = {}

        for row in reader:
            if row['District No'] not in districts:
                district = self._process_district(row)
                districts[district.number] = district
            if row['Sub District #'] not in subdistricts:
                subdistrict = self._process_subdistrict(row, districts[row['District No']])
                subdistricts[subdistrict.number] = subdistrict
            if row['Unit No'] not in sponsoring_organizations:
                subdistrict_number = subdistricts[row['District No'] + '-' + row['Sub District #']]
                sponsoring_organization = self._process_sponsoring_organization(row, subdistrict_number)
                sponsoring_organizations[sponsoring_organization.number] = sponsoring_organization

        return {
            'districts': districts,
            'subdistricts': subdistricts,
            'sponsoring_organizations': sponsoring_organizations,
        }

    def _process_district(self, data):
        """Process the data for a District

        Args:
            data: dict from file data
        Returns:
            District object
        """
        return self.district_factory.get_from_file_data(data)

    def _process_subdistrict(self, data, district):
        """Process the data for a Subdistrict

        Args:
            data: dict from file data
        Returns:
            Subdistrict object
        """
        return self.subdistrict_factory.get_from_file_data(data, district)

    def _process_sponsoring_organization(self, data, subdistrict):  # pylint: disable=invalid-name
        """Process the data for a Sponsoring Organization

        Args:
            data: dict from file data
        Returns:
            SponsoringOrganization object
        """
        return self.sponsoringorganization_factory.get_from_file_data(data, subdistrict)
