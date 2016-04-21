# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Youth Application API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from controllers import YouthApplication
from models import User
from models import Youth


def get_applications_by_status(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    status = event['status']
    return controller.get_applications_by_status(status)


def submit_application(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    app = controller.submit_application(app)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_guardian_approval(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    (app, youth) = controller.submit_guardian_approval(app, data)

    Youth.ApplicationPersister().save(app)
    if youth:
        Youth.YouthPersister().save(youth)

    return app.uuid


def submit_guardian_rejection(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = controller.submit_guardian_rejection(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_unit_approval(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = controller.submit_unit_approval(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_unit_rejection(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = controller.submit_unit_rejection(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def pay_fees(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = controller.pay_fees(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def mark_as_recorded(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    (app, youth) = controller.mark_as_recorded(app, data)
    Youth.ApplicationPersister().save(app)
    Youth.YouthPersister().save(youth)
    return app.uuid


def _get_controller(event, context):
    """Creates and returns the YouthApplication.Controller object"""
    user = User.Factory().load_by_session(context['session_id'])
    return YouthApplication.Controller(user)
