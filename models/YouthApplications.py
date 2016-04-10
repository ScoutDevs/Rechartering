""" YouthApplications classes """
from . import Base


STATUS_CREATED = 'Created'
STATUS_GUARDIAN_APPROVAL = 'Awaiting Guardian Approval'
STATUS_UNIT_APPROVAL = 'Awaiting Unit Approval'
STATUS_FEE_PENDING = 'Fee Payment Pending'
STATUS_READY_FOR_SCOUTNET = 'Ready for ScoutNet'
STATUS_COMPLETE = 'Complete'
STATUS_REJECTED = 'Rejected'


class YouthApplications(Base.Object):  # pylint: disable=too-many-instance-attributes
    """ YouthApplications class """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.unit_id = ''
        self.status = STATUS_CREATED
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

    def set_status(self, status):
        """ Set the application status """
        self.status = status

    def set_guardian_approval(self, approval):
        """ Set guardian approval """
        self.guardian_approval_guardian_id = approval['guardian_approval_guardian_id']
        self.guardian_approval_signature = approval['guardian_approval_signature']
        self.guardian_approval_date = approval['guardian_approval_date']

    def set_unit_approval(self, approval):
        """ Set unit approval """
        self.unit_approval_user_id = approval['unit_approval_user_id']
        self.unit_approval_signature = approval['unit_approval_signature']
        self.unit_approval_date = approval['unit_approval_date']

    def set_fee_payment(self, data):
        """ Set fee payment """
        self.fee_payment_date = data['fee_payment_date']
        self.fee_payment_user_id = data['fee_payment_user_id']
        self.fee_payment_receipt = data['fee_payment_receipt']

    def set_recorded_in_scoutnet(self, data):
        """ Mark as recorded in ScoutNet """
        self.scoutnet_id = data['scoutnet_id']
        self.recorded_in_scoutnet_date = data['date']

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
            STATUS_CREATED,
            STATUS_GUARDIAN_APPROVAL,
            STATUS_UNIT_APPROVAL,
            STATUS_FEE_PENDING,
            STATUS_READY_FOR_SCOUTNET,
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
        fields = {}
        if self.status in [STATUS_UNIT_APPROVAL, STATUS_FEE_PENDING, STATUS_READY_FOR_SCOUTNET, STATUS_COMPLETE]:
            fields.update({
                'guardian_approval_guardian_id': Base.FIELD_REQUIRED,
                'guardian_approval_signature': Base.FIELD_REQUIRED,
                'guardian_approval_date': Base.FIELD_REQUIRED,
            })
        if self.status in [STATUS_FEE_PENDING, STATUS_READY_FOR_SCOUTNET, STATUS_COMPLETE]:
            fields.update({
                'unit_approval_user_id': Base.FIELD_REQUIRED,
                'unit_approval_signature': Base.FIELD_REQUIRED,
                'unit_approval_date': Base.FIELD_REQUIRED,
            })
        if self.status in [STATUS_READY_FOR_SCOUTNET, STATUS_COMPLETE]:
            fields.update({
                # TODO: not required for LDS units; make conditional?
                # 'fee_payment_date': Base.FIELD_REQUIRED,
                # 'fee_payment_user_id': Base.FIELD_REQUIRED,
                # 'fee_payment_receipt': Base.FIELD_REQUIRED,
            })
        if self.status in [STATUS_COMPLETE]:
            fields.update({
                'recorded_in_scoutnet_date': Base.FIELD_REQUIRED,
            })
        if self.status == STATUS_REJECTED:
            fields.update({
                'rejection_date': Base.FIELD_REQUIRED,
                'rejection_reason': Base.FIELD_REQUIRED,
            })

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
