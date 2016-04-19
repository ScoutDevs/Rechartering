# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Organizations API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function

import urllib

import boto3

from controllers import Organization
from controllers import OrganizationImport
from models import Organization as OrganizationModel
from models import District
from models import SponsoringOrganization
from models import Subdistrict
from models import User


def get(event, context):
    """Lambda facade for Organization.Controller.get method"""
    controller = _get_controller(event, context)
    obj = controller.get(event['uuid'])
    return obj.__dict__


def search(event, context):
    """Lambda facade for Organization.Controller.search method"""
    controller = _get_controller(event, context)
    result = controller.search(event['search_data'])
    return result


def post(event, context):
    """Lambda facade for Organization.Controller.set method"""
    controller = _get_controller(event, context)
    obj = controller.set(event['data'])
    OrganizationModel.Persister().save(obj)
    return obj.__dict__


def put(event, context):
    """Lambda facade for Organization.Controller.update method"""
    controller = _get_controller(event, context)
    obj = controller.update(event['data'])
    OrganizationModel.Persister().save(obj)
    return obj.__dict__


def import_data(event, context):
    """Lambda facade for OrganizationImport.process_s3_object method"""
    s3_service = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        response = s3_service.get_object(Bucket=bucket, Key=key)
    except Exception as exc:
        print(exc)
        print('Error getting object {} from bucket {}.'.format(key, bucket))
        raise exc

    controller = _get_import_controller(event, context)
    data = controller.process_s3_object(response)
    num_processed = _store_data(data)

    return {
        'records_processed': num_processed,
    }


def _store_data(data):
    """Store the objects that have been processed"""
    num_processed = _store(data['districts'], District.Persister())
    num_processed = num_processed + _store(data['subdistricts'], Subdistrict.Persister())
    num_processed = num_processed + _store(data['sponsoring_organizations'], SponsoringOrganization.Persister())
    return num_processed


def _store(data, persister):
    """Store the objects"""
    num_processed = 0
    for obj in data:
        num_processed = num_processed + 1
        persister.save(obj)
    return num_processed


def _get_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(context['session_id'])
    return Organization.Controller(user)


def _get_import_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(context['session_id'])
    return OrganizationImport.Controller(user)
