# pylint: disable=unused-argument
""" AWS Lambda Handlers for the Youth Application API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function
from controllers import YouthApplication
from models import Youth
from aws import LambdaHelper

CONTROLLER = YouthApplication.Controller()


def find_duplicate_youth(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    youth_data = event['youth']
    return CONTROLLER.find_duplicate_youth(youth_data)


def get_applications_by_status(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    status = event['status']
    return CONTROLLER.get_applications_by_status(status)


def submit_application(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    app = CONTROLLER.submit_application(app)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_guardian_approval(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    (app, youth) = CONTROLLER.submit_guardian_approval(app, data)

    Youth.ApplicationPersister().save(app)
    if youth:
        Youth.YouthPersister().save(youth)

    return app.uuid


def submit_guardian_rejection(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = CONTROLLER.submit_guardian_rejection(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_unit_approval(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = CONTROLLER.submit_unit_approval(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def submit_unit_rejection(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = CONTROLLER.submit_unit_rejection(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def pay_fees(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    app = CONTROLLER.pay_fees(app, data)
    Youth.ApplicationPersister().save(app)
    return app.uuid


def mark_as_recorded(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    app = Youth.ApplicationFactory().load_by_uuid(event['application_id'])
    data = event['data']
    (app, youth) = CONTROLLER.mark_as_recorded(app, data)
    Youth.ApplicationPersister().save(app)
    Youth.YouthPersister().save(youth)
    return app.uuid


def revoke_guardian_approval(event, context):
    """ Lambda facade for YouthApplication.Controller method """
    guardian = event['guardian']
    youth = event['youth']
    return CONTROLLER.revoke_guardian_approval(guardian, youth)
