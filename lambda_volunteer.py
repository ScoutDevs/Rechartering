# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Volunteers API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function

from controllers import Volunteer
from models import Volunteer as VolunteerModel
from models import User


def get(event, context):
    """Lambda facade for Volunteer.Controller.get method"""
    controller = _get_controller(event, context)
    obj = controller.get(event['uuid'])
    return obj.to_dict()


def search(event, context):
    """Lambda facade for Volunteer.Controller.search method"""
    controller = _get_controller(event, context)
    result = controller.search(event['search_data'])
    return result


def post(event, context):
    """Lambda facade for Volunteer.Controller.set method"""
    controller = _get_controller(event, context)
    obj = controller.set(event['data'])
    VolunteerModel.Persister().save(obj)
    return obj.to_dict()


def put(event, context):
    """Lambda facade for Volunteer.Controller.update method"""
    controller = _get_controller(event, context)
    obj = controller.update(event['data'])
    VolunteerModel.Persister().save(obj)
    return obj.to_dict()


def _get_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(event['session_uuid'])
    return Volunteer.Controller(user)
