""" Youth Application controller """
from datetime import date
from models import Units
from models import Youth
from models import YouthApplications


class YouthApplication(object):
    """ Youth Application Controller """

    def __init__(self):
        """ init """
        self.factory = YouthApplications.Factory()
        self.persister = YouthApplications.Persister()

    @staticmethod
    def look_up_youth(youth_data):
        """ Search to see if the youth is already in the system """
        youth = Youth.Factory().construct(youth_data)
        duplicates = Youth.Persister().find_potential_duplicates(youth)
        return duplicates

    def get_applications_by_status(self, status):
        """ Load all applications matching the specified status """
        results = self.persister.get_by_status(status)
        return results

    def submit_application(self, app):
        """ Submit the application """
        self._enforce_app_status(app, YouthApplications.STATUS_CREATED)

        app.set_status(YouthApplications.STATUS_GUARDIAN_APPROVAL)

        if app.youth_id:
            app.scoutnet_id = self._get_youth_scoutnet_id(app)
            approval = self._get_guardian_approval(app)
            if approval:
                app = self.submit_guardian_approval(app, approval)

        app.validate()
        return app

    @staticmethod
    def _get_guardian_approval(app):
        """ Get the guardian approval on file """
        youth = Youth.Factory().load_by_uuid(app.youth_id)
        return youth.get_guardian_approval()

    @staticmethod
    def _get_youth_scoutnet_id(app):
        """ Get the scoutnet ID on file """
        youth = Youth.Factory().load_by_uuid(app.youth_id)
        return youth.scoutnet_id

    def submit_guardian_approval(self, app, approval):
        """ Submit guardian approval """
        self._enforce_app_status(app, YouthApplications.STATUS_GUARDIAN_APPROVAL)
        if 'guardian_approval_date' not in approval or not approval['guardian_approval_date']:
            approval['guardian_approval_date'] = date.today().isoformat()

        app.set_guardian_approval(approval)
        app.set_status(YouthApplications.STATUS_UNIT_APPROVAL)

        # LAMBDA-TODO: record on youth record

        app.validate()
        return app

    def submit_guardian_rejection(self, app, rejection):
        """ Submit guardian reject (non-approval) """
        # TODO: implement this
        pass

    def submit_unit_approval(self, app, approval):
        """ Submit unit approval """
        self._enforce_app_status(app, YouthApplications.STATUS_UNIT_APPROVAL)
        if 'unit_approval_date' not in approval or not approval['unit_approval_date']:
            approval['unit_approval_date'] = date.today().isoformat()

        app.set_unit_approval(approval)

        if self._is_application_for_lds_unit(app):
            app.set_status(YouthApplications.STATUS_READY_FOR_SCOUTNET)
        else:
            app.set_status(YouthApplications.STATUS_FEE_PENDING)

        app.validate()
        return app

    @staticmethod
    def _is_application_for_lds_unit(app):
        unit = Units.Factory().load_by_uuid(app.unit_id)
        return unit.lds_unit

    def submit_unit_rejection(self, app, rejection):
        """ Submit unit rejection (non-approval) """
        # TODO: implement this
        pass

    def pay_fees(self, app, data):
        """
        Mark fees as paid

        Usually done by a council employee
        """
        self._enforce_app_status(app, YouthApplications.STATUS_FEE_PENDING)
        if 'fee_payment_date' not in data or not data['fee_payment_date']:
            data['fee_payment_date'] = date.today().isoformat()

        app.set_fee_payment(data)
        app.set_status(YouthApplications.STATUS_READY_FOR_SCOUTNET)

        app.validate()
        return app

    def mark_as_recorded(self, app, data):
        """
        Mark the application as recorded in ScoutNet

        Usually done by a council employee
        """
        self._enforce_app_status(app, YouthApplications.STATUS_READY_FOR_SCOUTNET)
        if 'date' not in data:
            data['date'] = date.today().isoformat()

        # LAMBDA-TODO: create Youth record, or add unit to existing Youth record

        app.set_recorded_in_scoutnet(data)
        app.set_status(YouthApplications.STATUS_COMPLETE)

        app.validate()
        return app

    @staticmethod
    def _enforce_app_status(app, status):
        if app.status != status:
            raise InvalidActionException(
                'Can only submit guardian approval for applications in "{}" status; current status: "{}"'.
                format(
                    status,
                    app.status,
                )
            )


class InvalidActionException(Exception):
    """ The action attempted is not valid """
    pass
