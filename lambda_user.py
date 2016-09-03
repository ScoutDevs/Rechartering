# pylint: disable=unused-argument
"""AWS Lambda Handlers for the User API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function

from controllers import User
from lambda_base import get_session
from models import User as UserModel
from models import Session


def log_in(event, context):
    """Log the user in"""
    controller = User.Controller(None)

    user = controller.log_in(event['username'], event['password'])

    session = get_session(event)
    session.set('user_uuid', user.uuid)
    Session.Persister().save(session)

    response = {
        'uuid': user.uuid,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return response


def _get_controller(event, context):
    """Creates and returns the Controller object"""
    user = UserModel.Factory().load_by_session(event['session_uuid'])
    return User.Controller(user)
