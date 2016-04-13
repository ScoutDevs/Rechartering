# pylint: disable=no-member
""" Youth classes """
import hashlib
import re
from . import Base

APPLICATION_STATUS_CREATED = 'Created'
APPLICATION_STATUS_GUARDIAN_APPROVAL = 'Awaiting Guardian Approval'
APPLICATION_STATUS_UNIT_APPROVAL = 'Awaiting Unit Approval'
APPLICATION_STATUS_FEE_PENDING = 'Fee Payment Pending'
APPLICATION_STATUS_READY_FOR_SCOUTNET = 'Ready for ScoutNet'
APPLICATION_STATUS_COMPLETE = 'Complete'
APPLICATION_STATUS_REJECTED = 'Rejected'


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

    def get_validator(self):
        return YouthValidator(self)

    def get_record_hash(self):
        """ Hash the record for easy duplicate checks """
        regex = re.compile('[a-zA-Z0-9]+')
        match = regex.findall(self.first_name+self.last_name+self.date_of_birth)
        string = "".join(match)
        return hashlib.sha256(string).hexdigest()

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

    @staticmethod
    def get_factory():
        return YouthFactory()


class YouthValidator(Base.Validator):
    """ Youth validator """

    def prepare_for_validate(self):
        self.obj.duplicate_hash = self.obj.get_record_hash()

    def get_field_requirements(self):
        return {
            'uuid': Base.FIELD_REQUIRED,
            'duplicate_hash': Base.FIELD_REQUIRED,
            'units': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'date_of_birth': Base.FIELD_REQUIRED,
        }


class YouthFactory(Base.Factory):
    """ Youth Factory """

    def construct_from_app(self, app):
        """ Constructs a Youth object from the application """
        # construct will only populate fields that are defined in the class
        youth = self.construct(app.__dict__)
        # we don't want it to inherit the UUID from the app, though!
        youth.uuid = self.get_uuid()
        return youth

    @staticmethod
    def _get_uuid_prefix():
        return 'yth'

    @staticmethod
    def _get_object_class():
        return Youth

    @staticmethod
    def _get_persister():
        return YouthPersister()


class YouthPersister(Base.Persister):
    """ Persists Youth objects """

    @staticmethod
    def _get_table_name():
        return 'Youth'

    def find_potential_duplicates(self, youth):
        """ Find duplicates based on hash """
        return self.query(key='duplicate_hash', value=youth.get_record_hash())


class Application(Base.Object):  # pylint: disable=too-many-instance-attributes
    """ Youth Application class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.unit_id = ''
        self.status = APPLICATION_STATUS_CREATED
        self.guardian_approval_guardian_id = ''
        self.guardian_approval_signature = ''
        self.guardian_approval_date = ''
        self.unit_approval_user_id = ''
        self.unit_approval_signature = ''
        self.unit_approval_date = ''
        self.fee_payment_date = ''
        self.fee_payment_user_id = ''
        self.fee_payment_receipt = ''
        self.recorded_in_scoutnet_date = ''
        self.rejection_date = ''
        self.rejection_reason = ''
        self.youth_id = ''
        self.scoutnet_id = 0
        self.first_name = ''
        self.last_name = ''
        self.date_of_birth = ''

    def get_validator(self):
        return ApplicationValidator(self)

    @staticmethod
    def get_factory():
        return ApplicationFactory()


class ApplicationValidator(Base.Validator):
    """ Youth Application validator """

    def get_field_requirements(self):
        field_requirements = {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'unit_id': Base.FIELD_REQUIRED,
            'first_name': Base.FIELD_REQUIRED,
            'last_name': Base.FIELD_REQUIRED,
            'date_of_birth': Base.FIELD_REQUIRED,
        }
        status_field_requirements = ApplicationStatusValidator(self.obj.status).get_field_requirements()
        field_requirements.update(status_field_requirements)
        return field_requirements

    @staticmethod
    def get_valid_statuses():
        """ List of all valid statuses """
        return [
            APPLICATION_STATUS_CREATED,
            APPLICATION_STATUS_GUARDIAN_APPROVAL,
            APPLICATION_STATUS_UNIT_APPROVAL,
            APPLICATION_STATUS_FEE_PENDING,
            APPLICATION_STATUS_READY_FOR_SCOUTNET,
            APPLICATION_STATUS_COMPLETE,
            APPLICATION_STATUS_REJECTED,
        ]

    def _validate(self):
        (valid, errors) = super(self.__class__, self)._validate()
        if self.obj.status not in self.get_valid_statuses():
            errors.append('Invalid status "{}"'.format(self.obj.status))
            valid = False

        return (valid, errors)


class ApplicationStatusValidator(object):  # pylint: disable=too-few-public-methods
    """ Validation based on the application status """

    def __init__(self, status):
        self.status = status

    def get_field_requirements(self):
        """ Additional field requirements by status """
        fields = {}
        if self.status in [
                APPLICATION_STATUS_UNIT_APPROVAL,
                APPLICATION_STATUS_FEE_PENDING,
                APPLICATION_STATUS_READY_FOR_SCOUTNET,
                APPLICATION_STATUS_COMPLETE]:
            fields.update({
                'guardian_approval_guardian_id': Base.FIELD_REQUIRED,
                'guardian_approval_signature': Base.FIELD_REQUIRED,
                'guardian_approval_date': Base.FIELD_REQUIRED,
            })
        if self.status in [
                APPLICATION_STATUS_FEE_PENDING,
                APPLICATION_STATUS_READY_FOR_SCOUTNET,
                APPLICATION_STATUS_COMPLETE]:
            fields.update({
                'unit_approval_user_id': Base.FIELD_REQUIRED,
                'unit_approval_signature': Base.FIELD_REQUIRED,
                'unit_approval_date': Base.FIELD_REQUIRED,
            })
        if self.status in [APPLICATION_STATUS_READY_FOR_SCOUTNET, APPLICATION_STATUS_COMPLETE]:
            fields.update({})
        if self.status in [APPLICATION_STATUS_COMPLETE]:
            fields.update({
                'recorded_in_scoutnet_date': Base.FIELD_REQUIRED,
            })
        if self.status == APPLICATION_STATUS_REJECTED:
            fields.update({
                'rejection_date': Base.FIELD_REQUIRED,
                'rejection_reason': Base.FIELD_REQUIRED,
            })

        return fields


class ApplicationFactory(Base.Factory):
    """ Youth Application Factory """

    @staticmethod
    def _get_uuid_prefix():
        return 'yap'

    @staticmethod
    def _get_object_class():
        return Application

    @staticmethod
    def _get_persister():
        return ApplicationPersister()


class ApplicationPersister(Base.Persister):

    """ Persists Youth Application objects """

    @staticmethod
    def _get_table_name():
        return 'YouthApplications'

    def get_by_status(self, status):
        """ Return applications matching the specified status """
        return self.query(key='status', value=status)
