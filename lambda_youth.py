# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Youth API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from controllers import Youth
from models import User


def find_duplicate_youth(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    youth_data = event['youth']
    return controller.find_duplicate_youth(youth_data)


def revoke_guardian_approval(event, context):
    """Lambda facade for YouthApplication.Controller method"""
    controller = _get_controller(event, context)
    guardian = event['guardian']
    youth = event['youth']
    return controller.revoke_guardian_approval(guardian, youth)


def _get_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(event['session_uuid'])
    return Youth.Controller(user)
