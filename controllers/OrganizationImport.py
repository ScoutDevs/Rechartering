# pylint: disable=import-error
"""Organization Import Controller"""

import csv
import StringIO

from models import District
from models import SponsoringOrganization
from models import Subdistrict

from . import ClientErrorException


class Controller(object):
    """Organization Import Controller

    'Organization' in this case includes districts, subdistricts, and
    sponsoring organizations.

    The Council keeps a list of the various organizations in spreadsheet.
    This will take a TSV (tab-separated values) file, process it, and
    give back a dict with all the objects with relationships defined.
    """

    def __init__(self,
                 district_factory=None,
                 subdistrict_factory=None,
                 sporg_factory=None):
        if district_factory:
            self.district_factory = district_factory
        else:
            self.district_factory = District.Factory()

        if subdistrict_factory:
            self.subdistrict_factory = subdistrict_factory
        else:
            self.subdistrict_factory = Subdistrict.Factory()

        if sporg_factory:
            self.sporg_factory = sporg_factory
        else:
            self.sporg_factory = SponsoringOrganization.Factory()

    def process_s3_object(self, s3_object):
        """Process the data as it comes in from S3

        Args:
            s3_object: boto3 s3_object object
        Yields:
            tuple: of district, subdistrict, and sporg
        """
        data = s3_object['Body'].read()
        data_file = StringIO.StringIO(data)
        for record in self._process_file(data_file):
            yield record

    def process_file(self, filename):
        """Process the data as it comes in from a local file

        Args:
            filename: name of local file
        Yields:
            dict
        """
        with open(filename) as data_file:
            for record in self._process_file(data_file):
                yield record

    def _process_file(self, data_file):
        """Processes the data file provided by the council

        The council can drop off a data file into an S3 bucket for processing.
        That action kicks off a Lambda function which calls this method.  The
        file the council provides is a tab-delimited flat file with the following
        fields:
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
        Yields:
            dict
        """
        reader = csv.DictReader(data_file, dialect=csv.excel_tab)
        self._validate_headers(reader)

        row_num = 1
        for row in reader:
            row_num = row_num + 1

            if not self._is_valid_record(row):
                continue

            record = {
                'district_number': row['District No'],
                'district_name': row['District Name'],
                'subdistrict_number': row['District No'] + '-' + row['Sub District #'],
                'subdistrict_name': row['Stake/Sub District Name'],
                'sporg_name': row['Ward/Sponsoring Org'],
                'sporg_number': row['Unit No'],
            }

            yield record

    @staticmethod
    def _validate_headers(reader):
        for header in Controller._get_required_headers():
            if header not in reader.fieldnames:
                raise ClientErrorException('Invalid file format.  Header "'+header+'" not found.')

    @staticmethod
    def _get_required_headers():
        return [
            'District No',
            'District Name',
            'Sub District #',
            'Stake/Sub District Name',
            'Unit No',
            'Ward/Sponsoring Org',
        ]

    @staticmethod
    def _is_valid_record(row):
        valid = True
        for header in Controller._get_required_headers():
            if not row[header]:
                valid = False
                break
        return valid

    def process_record(self, record):
        """Processes an organization file record as provided by the council

        Args:
            record: dict
        Returns:
            tuple: district, subdistrict, sporg objects
        """
        # TO-DO: This needs to be injectable, since the UNPC approach doesn't
        # appear to be a standard
        district = self._process_district(record)
        subdistrict = self._process_subdistrict(record, district)
        sporg = self._process_sponsoring_organization(record, subdistrict)
        return (district, subdistrict, sporg)

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
            sporg object
        """
        return self.sporg_factory.get_from_file_data(data, subdistrict)
