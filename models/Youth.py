# pylint: disable=no-member
""" Youth classes """
import hashlib
import re
from . import Base


class Youth(Base.Object):  # pylint: disable=too-many-instance-attributes
    """ Youth class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.duplicate_hash = ''
        self.units = []
        self.scoutnet_id = ''
        self.application_id = ''
        self.guardians = []
        self.first_name = ''
        self.last_name = ''
        self.date_of_birth = ''
        self.guardian_approval_guardian_id = ''
        self.guardian_approval_signature = ''
        self.guardian_approval_date = ''

    @staticmethod
    def get_uuid_prefix():
        return 'yth'

    def get_validator(self):
        return Validator(self)

    def get_record_hash(self):
        """ Hash the record for easy duplicate checks """
        regex = re.compile('[a-zA-Z0-9]+')
        match = regex.findall(self.first_name+self.last_name+self.date_of_birth)
        string = "".join(match)
        return hashlib.sha256(string).hexdigest()

    def prepare_for_validate(self):
        self.duplicate_hash = self.get_record_hash()

    def get_guardian_approval(self):
        """ Get guardian approval data """
        approval = {}
        if self.guardian_approval_guardian_id:
            approval = {
                'guardian_approval_guardian_id': self.guardian_approval_guardian_id,
                'guardian_approval_signature': self.guardian_approval_signature,
                'guardian_approval_date': self.guardian_approval_date,
            }
        return approval


class Validator(Base.Validator):
    """ Youth validator """

    @staticmethod
    def get_field_requirements():
        return {
            'uuid': Base.FIELD_REQUIRED,
            'duplicate_hash': Base.FIELD_REQUIRED,
            'units': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'date_of_birth': Base.FIELD_REQUIRED,
        }


class Factory(Base.Factory):
    """ Youth Factory """

    @staticmethod
    def _get_object_class():
        return Youth

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):
    """ Persists Youth objects """

    @staticmethod
    def _get_table_name():
        return 'Youth'

    def find_potential_duplicates(self, youth):
        """ Find duplicates based on hash """
        return self.query(key='duplicate_hash', value=youth.get_record_hash())
