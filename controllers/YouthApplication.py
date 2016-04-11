# pylint: disable=import-error
# TODO: implement security measures
""" Youth Application controller """
from datetime import date
from controllers import InvalidActionException
from models import Unit
from models import Youth


class Controller(object):
    """Youth Application Controller

    Manages the Youth Application workflow from beginning to end, top to
    bottom.

    Attributes:
        factory: Application factory object
        persister: Application persister object
        unit: Unit object
    """

    def __init__(self, application_persister=None, unit_factory=None):
        """ init """
        self.factory = Youth.ApplicationFactory()
        if application_persister:
            self.persister = application_persister
        else:
            self.persister = Youth.ApplicationPersister()

        if unit_factory:
            self.unit_factory = unit_factory
        else:
            self.unit_factory = Unit.Persister()

    @staticmethod
    def find_duplicate_youth(youth_data):
        """Search to see if the youth is already in the system

        Duplicate records for the same individual are to be avoided as much
        as possible. This will check for duplicate youth already in the
        system, allowing the user to submit an application using an existing
        record rather than creating new one.

        Args:
            youth_data: dict containing the data describing the Youth
        Returns:
            List of Youth records who are potential duplicates
        """
        youth = Youth.Factory().construct(youth_data)
        duplicates = Youth.Persister().find_potential_duplicates(youth)
        return duplicates

    def get_applications_by_status(self, status):
        """Load all applications matching the specified status

        Args:
            status: string containing the status to search for
        Returns:
            List of Applications matching the specified status
        """
        results = self.persister.get_by_status(status)
        return results

    def submit_application(self, app):
        """Submit the application

        This handles the initial application submission, and sets the status
        to GUARDIAN_APPROVAL, or to UNIT_APPROVAL if the guardian approval
        is already on record.

        Args:
            app: New Application object to submit
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_CREATED)

        app.status = Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL

        if app.youth_id:
            app.scoutnet_id = self._get_youth_scoutnet_id(app)
            approval = self._get_guardian_approval(app)
            if approval:
                app = self.submit_guardian_approval(app, approval)

        app.validate()
        return app

    @staticmethod
    def _get_guardian_approval(app):
        """ Get the guardian approval on file

        If the user found an existing youth record to submit the application
        for, then it's possible the guardian's approval could be on file.
        This will attempt to find it.

        Args:
            app: Application object to check
        Returns:
            dict containing approval data, or empty dict
        """
        youth = Youth.Factory().load_by_uuid(app.youth_id)
        return youth.get_guardian_approval()

    @staticmethod
    def _get_youth_scoutnet_id(app):
        """Get the ScoutNet ID on file

        If the scout already exists in the system, this will find the ScoutNet
        ID and apply it to this application for easy retrieval by the Council
        staff.

        Args:
            app: Application object
        Returns:
            int: the Youth's ScoutNet ID
        """
        youth = Youth.Factory().load_by_uuid(app.youth_id)
        return youth.scoutnet_id

    def submit_guardian_approval(self, app, data):
        """Submit guardian approval

        After the form is initially submitted, a parent or guardian must
        indicate their approval for the youth to participate in the BSA
        program.  This handles the submission of that approval.

        Args:
            app: Application object in GUARDIAN_APPROVAL status
            data: dict containing the following fields:
                guardian_approval_guardian_id: ID of the guardian who granted
                    approval
                guardian_approval_signature: signature provided by guardian
                guardian_approval_date (optional): date of original guardian
                    approval for the youth; defaults to current date
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL)
        if 'guardian_approval_date' not in data or not data['guardian_approval_date']:
            data['guardian_approval_date'] = date.today().isoformat()

        app.guardian_approval_guardian_id = data['guardian_approval_guardian_id']
        app.guardian_approval_signature = data['guardian_approval_signature']
        app.guardian_approval_date = data['guardian_approval_date']
        app.status = Youth.APPLICATION_STATUS_UNIT_APPROVAL

        # LAMBDA-TODO: record on youth record

        app.validate()
        return app

    def submit_guardian_rejection(self, app, data):
        """Submit guardian reject (non-approval)

        If the guardian opts to NOT allow their youth to participate in the
        BSA, this allows them to so indicate.  This applies to only this
        specific application.  If the user wants to revoke permission more
        permanently for their youth, use the revoke_guardian_approval method.

        Args:
            app: Application object in GUARDIAN_APPROVAL status
            data: dict containing the following fields:
                rejection_reason (optional): ID of the guardian who granted
                    approval; default message is used if not provided
                rejection_date (optional): defaults to current date
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL)
        if 'rejection_reason' not in data:
            data['rejection_reason'] = 'Guardian approval NOT granted'
        if 'rejection_date' not in data:
            data['rejection_date'] = date.today().isoformat()

        app.rejection_reason = data['rejection_reason']
        app.rejection_date = data['rejection_date']

        app.status = Youth.APPLICATION_STATUS_REJECTED

        app.validate()
        return app

    def submit_unit_approval(self, app, data):
        """Submit unit approval

        After the guardian has provided approval, the unit must approve the
        application.

        Args:
            app: Application object in UNIT_APPROVAL status
            data: dict containing the following fields:
                unit_approval_user_id: User ID of the user who approved
                unit_approval_signature: Signature of said user
                unit_approval_date (optional): defaults to current date
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_UNIT_APPROVAL)
        if 'unit_approval_date' not in data or not data['unit_approval_date']:
            data['unit_approval_date'] = date.today().isoformat()

        app.unit_approval_user_id = data['unit_approval_user_id']
        app.unit_approval_signature = data['unit_approval_signature']
        app.unit_approval_date = data['unit_approval_date']

        if self._is_lds_unit_application(app):
            app.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET
        else:
            app.status = Youth.APPLICATION_STATUS_FEE_PENDING

        app.validate()
        return app

    def _is_lds_unit_application(self, app):
        """Determines whether the application is for an LDS unit

        Fees for LDS units are paid directly by the LDS Church at a national
        level, so they bypass the FEE_PENDING status.

        Args:
            app: Application object
        Returns:
            boolean
        """
        unit = self.unit_factory.load_by_uuid(app.unit_id)
        return unit.lds_unit

    def submit_unit_rejection(self, app, data):
        """Submit unit rejection (non-approval)

        In case of clerical error, change of address, etc., the unit may
        want to reject an application for their unit.

        Args:
            app: Application object in GUARDIAN_APPROVAL status
            data: dict containing the following fields:
                rejection_reason (optional): ID of the guardian who granted
                    approval; default message is used if not provided
                rejection_date (optional): defaults to current date
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_UNIT_APPROVAL)
        if 'rejection_reason' not in data:
            data['rejection_reason'] = 'Guardian approval NOT granted'
        if 'rejection_date' not in data:
            data['rejection_date'] = date.today().isoformat()

        app.rejection_reason = data['rejection_reason']
        app.rejection_date = data['rejection_date']

        app.status = Youth.APPLICATION_STATUS_REJECTED

        app.validate()
        return app

    def pay_fees(self, app, data):
        """Mark registration fees as paid

        Non-LDS units must pay the council directly to register youth.  Once the
        fee has been paid, a council employee can mark it as paid.

        Args:
            app: Application object in FEE_PENDING status
            data: dict containing the following fields:
                fee_payment_user_id (optional): ID of the user who is marking the
                    registration fees as paid
                fee_payment_receipt: Transaction or receipt number
                fee_payment_date (optional): defaults to current date
        Returns:
            Application object (updated)
        """
        # QUESTION: is this paid only annually?  Should we move past this...
        # automatically if the fee has already been paid for this youth? Does it
        # apply for the youth regardless of unit, or just for the youth + unit?

        # QUESTION: is there some sort of transaction ID or receipt or something we can record here?

        self._enforce_app_status(app, Youth.APPLICATION_STATUS_FEE_PENDING)
        if 'fee_payment_date' not in data or not data['fee_payment_date']:
            data['fee_payment_date'] = date.today().isoformat()

        app.fee_payment_date = data['fee_payment_date']
        app.fee_payment_user_id = data['fee_payment_user_id']
        app.fee_payment_receipt = data['fee_payment_receipt']
        app.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET

        app.validate()
        return app

    def mark_as_recorded(self, app, data):
        """Mark the application as recorded in ScoutNet

        Once everything is approved & paid for, the application is ready to be
        entered into ScoutNet.  Once it has been entered into ScoutNet, a
        Council employee will mark it as entered.

        Args:
            app: Application object in READY_FOR_SCOUTNET status
            data: dict containing the following fields:
                scoutnet_id (optional): ScoutNet ID for the Youth created.  Not
                    required for non-new youth.
                recorded_in_scoutnet_date (optional): defaults to current date
        Returns:
            Application object (updated)
        """
        self._enforce_app_status(app, Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET)
        if 'date' not in data:
            data['date'] = date.today().isoformat()

        # LAMBDA-TODO: create Youth record, or add unit to existing Youth record

        app.scoutnet_id = data['scoutnet_id']
        app.recorded_in_scoutnet_date = data['date']
        app.status = Youth.APPLICATION_STATUS_COMPLETE

        app.validate()
        return app

    @staticmethod
    def revoke_guardian_approval(guardian, youth):
        """Revokes guardian approval for the specified Youth

        If a guardian wishes to revoke their approval for a youth, they have
        that option.

        Args:
            guardian: Guardian object representing the guardian revoking approval
            youth: Youth whose approval is being revoked
        Raises:
            InvalidActionException: when guardian doesn't match youth's approval
        Returns:
            Youth object (updated)
        """
        if guardian.id == youth.guardian_approval_guardian_id:
            youth.guardian_approval_guardian_id = ''
            youth.guardian_approval_signature = ''
            youth.guardian_approval_date = ''
            return youth
        else:
            raise InvalidActionException('Only the guardian who granted approval can revoke it.')

    @staticmethod
    def _enforce_app_status(app, status):
        """Enforces proper workflow

        Specific actions are only allowed at specific times.  This will throw
        an exception if the app isn't in the specified status.

        Args:
            app: Application object
            status: Status to enforce
        Raises:
            InvalidActionException
        """
        if app.status != status:
            raise InvalidActionException(
                'Can only submit guardian approval for applications in "{}" status; current status: "{}"'.
                format(
                    status,
                    app.status,
                )
            )
