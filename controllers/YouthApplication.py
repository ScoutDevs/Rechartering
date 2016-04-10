""" Youth Application controller """
from datetime import date
from models import Youth
from models import YouthApplications


class YouthApplication(object):
    """ Youth Application Controller """

    def __init__(self):
        """ init """
        self.factory = YouthApplications.Factory()
        self.persister = YouthApplications.Persister()

    def look_up_youth(self, youth_data):
        """ Search to see if the youth is already in the system """
        youth = Youth.Factory().construct(youth_data)
        duplicates = Youth.Factory().find_potential_duplicates(youth)
        return duplicates

    def get_applications_by_status(self, status):
        """ Load all applications matching the specified status """
        results = self.persister.get_by_status(status)
        return results

    def submit_application(self, app_data):
        """ Submit the application """
        app = self.factory.construct(app_data)
        app.set_status(YouthApplications.STATUS_GUARDIAN_APPROVAL)

        if hasattr(app, 'youth_id'):
            approval = self._get_guardian_approval(app.youth_id)
            if approval:
                app.set_guardian_approval(approval)
                app.set_status(YouthApplications.STATUS_UNIT_APPROVAL)

        app.validate()
        return app

    def _get_guardian_approval(self, app):
        """ Get the guardian approval on file """
        youth = Youth.Factory().load_by_uuid(app.youth_id)
        return youth.get_guardian_approval()

    def submit_guardian_approval(self, app, approval):
        """ Submit guardian approval """
        if 'date' not in approval:
            approval['date'] = date.today().isoformat()

        app.set_guardian_approval(approval)
        app.set_status(YouthApplications.STATUS_SUBMITTED)

        uuid = self.persister.save(app)
        return uuid

    def submit_guardian_rejection(self, app, rejection):
        """ Submit guardian reject (non-approval) """
        # TODO: implement this
        pass

    def submit_unit_approval(self, app, approval):
        """ Submit unit approval """
        if 'date' not in approval:
            approval['date'] = date.today().isoformat()

        app.set_guardian_approval(approval)
        app.set_status(YouthApplications.STATUS_SUBMITTED)

        app.validate()
        return app

    def submit_unit_rejection(self, app, rejection):
        """ Submit unit rejection (non-approval) """
        # TODO: implement this
        pass

    def pay_fees(self, application, receipt_id):
        """
        Mark fees as paid

        Usually done by a council employee
        """
        # TODO: implement this
        pass

    def mark_as_recorded(self, application, scoutnet_id):
        """
        Mark the application as recorded in ScoutNet

        Usually done by a council employee
        """
        # TODO: implement this
        pass
