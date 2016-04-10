""" YouthApplications classes """
from . import Base


STATUS_SUBMITTED = 'Submitted'
STATUS_GUARDIAN_APPROVAL = 'Awaiting Guardian Approval'
STATUS_UNIT_APPROVAL = 'Awaiting Unit Approval'
STATUS_FEE_PENDING = 'Fee Payment Pending'
STATUS_READY_TO_RECORD = 'Ready to Record'
STATUS_COMPLETE = 'Complete'
STATUS_REJECTED = 'Rejected'


class YouthApplications(Base.Object):  # pylint: disable=too-many-instance-attributes
    """ YouthApplications class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.unit_id = ''
        self.status = ''
        self.guardian_approval_guardian_id = ''
        self.guardian_approval_signature = ''
        self.guardian_approval_date = ''
        self.unit_approval_user_id = ''
        self.unit_approval_signature = ''
        self.unit_approval_date = ''
        self.fee_payment_date = ''
        self.fee_payment_user_id = ''
        self.fee_payment_signature = ''
        self.recorded_in_scoutnet_date = ''
        self.rejection_date = ''
        self.rejection_reason = ''

    def set_status(self, status):
        """ Set the application status """
        self.status = status

    def set_guardian_approval(self, approval):
        """ Set guardian approval """
        self.guardian_approval_guardian_id = approval.guardian_id
        self.guardian_approval_signature = approval.guardian_signature

    @staticmethod
    def get_uuid_prefix():
        return 'yap'

    def get_validator(self):
        return Validator(self)


class Validator(Base.Validator):
    """ YouthApplication validator """

    def get_field_requirements(self):
        field_requirements = {
            'uuid': Base.FIELD_REQUIRED,
            'status': Base.FIELD_REQUIRED,
            'unit_id': Base.FIELD_REQUIRED,
        }
        status_field_requirements = StatusValidator(self.obj.status).get_field_requirements()
        field_requirements.update(status_field_requirements)
        return field_requirements

    @staticmethod
    def get_valid_statuses():
        """ List of all valid statuses """
        return [
            STATUS_SUBMITTED,
            STATUS_GUARDIAN_APPROVAL,
            STATUS_UNIT_APPROVAL,
            STATUS_FEE_PENDING,
            STATUS_READY_TO_RECORD,
            STATUS_COMPLETE,
            STATUS_REJECTED,
        ]

    def _validate(self):
        (valid, errors) = super(Validator, self)._validate()
        if self.obj.status not in self.get_valid_statuses():
            errors.append('Invalid status "{}"'.format(self.obj.status))
            valid = False

        return (valid, errors)


class StatusValidator(object):  # pylint: disable=too-few-public-methods
    """ Validation based on the application status """

    def __init__(self, status):
        self.status = status

    def get_field_requirements(self):
        """ Additional field requirements by status """
        if self.status == STATUS_UNIT_APPROVAL:
            fields = {
                'guardian_approval_guardian_id': Base.FIELD_REQUIRED,
                'guardian_approval_signature': Base.FIELD_REQUIRED,
                'guardian_approval_date': Base.FIELD_REQUIRED,
            }
        elif self.status == STATUS_FEE_PENDING:
            fields = {
                'unit_approval_user_id': Base.FIELD_REQUIRED,
                'unit_approval_signature': Base.FIELD_REQUIRED,
                'unit_approval_date': Base.FIELD_REQUIRED,
            }
        elif self.status == STATUS_READY_TO_RECORD:
            fields = {
                'fee_payment_date': Base.FIELD_REQUIRED,
                'fee_payment_user_id': Base.FIELD_REQUIRED,
                'fee_payment_signature': Base.FIELD_REQUIRED,
            }
        elif self.status == STATUS_COMPLETE:
            fields = {
                'recorded_in_scoutnet_date': Base.FIELD_REQUIRED,
            }
        elif self.status == STATUS_REJECTED:
            fields = {
                'rejection_date': Base.FIELD_REQUIRED,
                'rejection_reason': Base.FIELD_REQUIRED,
            }
        else:
            fields = {}

        return fields


class Factory(Base.Factory):

    """ YouthApplications Factory """

    @staticmethod
    def _get_object_class():
        return YouthApplications

    @staticmethod
    def _get_persister():
        return Persister()


class Persister(Base.Persister):

    """ Persists YouthApplications objects """

    @staticmethod
    def _get_table_name():
        return 'YouthApplications'

    def get_by_status(self, status):
        """ Return applications matching the specified status """
        return self.query(key='status', value=status)
