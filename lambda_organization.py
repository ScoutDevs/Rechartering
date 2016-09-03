# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Organizations API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function

import json
import urllib

import boto3

from controllers import Organization
from controllers import OrganizationImport
from models import Organization as OrganizationModel
from models import District
from models import SponsoringOrganization
from models import Subdistrict
from models import User

TOPIC_ARN = 'arn:aws:sns:us-west-2:480058411585:organization_update'
SNS = boto3.client('sns')


def get(event, context):
    """Lambda facade for Organization.Controller.get method"""
    controller = _get_controller(event, context)
    obj = controller.get(event['uuid'])
    return obj.to_dict()


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
    return obj.to_dict()


def put(event, context):
    """Lambda facade for Organization.Controller.update method"""
    controller = _get_controller(event, context)
    obj = controller.update(event['data'])
    OrganizationModel.Persister().save(obj)
    return obj.to_dict()


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

    num_processed = 0

    for record in controller.process_s3_object(response):
        _queue_update(record)
        num_processed = num_processed + 1
        if 'test' in event['Records'][0] and num_processed >= 100:
            break

    response = {
        'records_processed': num_processed,
    }
    print(response)
    return response


def _queue_update(data):
    SNS.publish(
        TopicArn=TOPIC_ARN,
        Subject='Organization update message',
        Message=json.dumps(data),
    )


def process_record(event, context):
    """Lambda facade for Organization.Controller.process_record method"""
    controller = _get_import_controller(event, context)
    message = event['Records'][0]['Sns']['Message']
    data = json.loads(message)

    (district, subdistrict, sporg) = controller.process_record(data)

    District.Persister().save(district)
    Subdistrict.Persister().save(subdistrict)
    SponsoringOrganization.Persister().save(sporg)
    return ''


def _get_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(event['session_uuid'])
    return Organization.Controller(user)


def _get_import_controller(event, context):
    """Creates and returns the Controller object"""
    return OrganizationImport.Controller()
