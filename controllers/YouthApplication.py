# pylint: disable=import-error
"""Youth Application Controller"""

from datetime import date

from models import Unit
from models import Youth

from . import Youth as YouthController
from . import require_status
from .Security import require_role


class Controller(object):
    """Youth Application Controller

    Manages the Youth Application workflow from beginning to end, top to
    bottom.

    Attributes:
        factory: Application factory object
        persister: Application persister object
        unit: Unit object
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 user,
                 application_factory=None,
                 unit_factory=None,
                 youth_factory=None):
        """Dependency-injectable init

        Args:
            user: User object, used to determine permissions
            application_factory: Youth Application factory object
            unit_factory: Unit factory object
            youth_factory: Youth factory object
        """
        self.user = user
        if application_factory:
            self.factory = application_factory
        else:
            self.factory = Youth.ApplicationFactory()

        self.persister = self.factory.get_persister()

        if unit_factory:
            self.unit_factory = unit_factory
        else:
            self.unit_factory = Unit.Factory()

        if youth_factory:
            self.youth_factory = youth_factory
        else:
            youth_factory = Youth.YouthFactory()

    @require_role('Council.Employee')
    def get_applications_by_status(self, status):
        """Load all applications matching the specified status

        Args:
            status: string containing the status to search for
        Returns:
            List of Applications matching the specified status
        """
        results = self.persister.get_by_status(status)
        return results

    # No specific rights required to submit an application
    @require_status(Youth.APPLICATION_STATUS_CREATED)
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
        app.status = Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL

        if app.youth_id:
            app.scoutnet_id = self._get_youth_scoutnet_id(app)
            approval = self._get_guardian_approval(app)
            if approval:
                (app, _) = self.submit_guardian_approval(app, approval)

        app.validate()
        return app

    def _get_guardian_approval(self, app):
        """Get the guardian approval on file

        If the user found an existing youth record to submit the application
        for, then it's possible the guardian's approval could be on file.
        This will attempt to find it.

        Args:
            app: Application object to check
        Returns:
            dict containing approval data, or empty dict
        """
        youth = self.youth_factory.load_by_uuid(app.youth_id)
        return youth.get_guardian_approval()

    @require_role('Guardian')
    @require_status(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL)
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
            tuple: Application object (updated),
                and Youth object (possibly updated; None if no youth_id)
        Raises:
            RecordNotFoundException
        """
        if 'guardian_approval_date' not in data or not data['guardian_approval_date']:
            data['guardian_approval_date'] = date.today().isoformat()

        app.guardian_approval_guardian_id = data['guardian_approval_guardian_id']
        app.guardian_approval_signature = data['guardian_approval_signature']
        app.guardian_approval_date = data['guardian_approval_date']
        app.status = Youth.APPLICATION_STATUS_UNIT_APPROVAL

        if app.youth_id:
            youth = self.youth_factory.load_by_uuid(app.youth_id)
            controller = YouthController.Controller(self.user, self.youth_factory)
            youth = controller.grant_guardian_approval(youth, data)
            youth.validate()
        else:
            youth = None

        app.validate()
        return (app, youth)

    @require_role('Guardian')
    @require_status(Youth.APPLICATION_STATUS_GUARDIAN_APPROVAL)
    def submit_guardian_rejection(self, app, data):  # pylint: disable=no-self-use
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
        if 'rejection_reason' not in data:
            data['rejection_reason'] = 'Guardian approval NOT granted'
        if 'rejection_date' not in data:
            data['rejection_date'] = date.today().isoformat()

        app.rejection_reason = data['rejection_reason']
        app.rejection_date = data['rejection_date']

        app.status = Youth.APPLICATION_STATUS_REJECTED

        app.validate()
        return app

    @require_role(['Unit.Admin'])
    @require_status(Youth.APPLICATION_STATUS_UNIT_APPROVAL)
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

    @require_role('Unit.Admin')
    @require_status(Youth.APPLICATION_STATUS_UNIT_APPROVAL)
    def submit_unit_rejection(self, app, data):  # pylint: disable=no-self-use
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
        if 'rejection_reason' not in data:
            data['rejection_reason'] = 'Guardian approval NOT granted'
        if 'rejection_date' not in data:
            data['rejection_date'] = date.today().isoformat()

        app.rejection_reason = data['rejection_reason']
        app.rejection_date = data['rejection_date']

        app.status = Youth.APPLICATION_STATUS_REJECTED

        app.validate()
        return app

    @require_role('Council.Employee')
    @require_status(Youth.APPLICATION_STATUS_FEE_PENDING)
    def pay_fees(self, app, data):  # pylint: disable=no-self-use
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

        if 'fee_payment_date' not in data or not data['fee_payment_date']:
            data['fee_payment_date'] = date.today().isoformat()

        app.fee_payment_date = data['fee_payment_date']
        app.fee_payment_user_id = data['fee_payment_user_id']
        app.fee_payment_receipt = data['fee_payment_receipt']
        app.status = Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET

        app.validate()
        return app

    @require_role('Council.Employee')
    @require_status(Youth.APPLICATION_STATUS_READY_FOR_SCOUTNET)
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
        if 'date' not in data:
            data['date'] = date.today().isoformat()

        app.scoutnet_id = data['scoutnet_id']
        app.recorded_in_scoutnet_date = data['date']
        app.status = Youth.APPLICATION_STATUS_COMPLETE

        if app.youth_id:
            youth = self.youth_factory.load_by_uuid(app.youth_id)
        else:
            youth = self.youth_factory.construct_from_app(app)
        youth.units.append(app.unit_id)

        app.validate()
        youth.validate()
        return app

    def _get_youth_scoutnet_id(self, app):
        """Get the ScoutNet ID on file

        If the scout already exists in the system, this will find the ScoutNet
        ID and apply it to this application for easy retrieval by the Council
        staff.

        Args:
            app: Application object
        Returns:
            int: the Youth's ScoutNet ID
        """
        youth = self.youth_factory.load_by_uuid(app.youth_id)
        return youth.scoutnet_id
