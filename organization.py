# pylint: disable=unused-argument
"""AWS Lambda Handlers for the Organizations API

AWS Lambda needs nice, clean hooks.  This file provides those.
"""
from __future__ import print_function
import boto3
import urllib
from controllers import OrganizationImport
from models import User


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
    controller.process_s3_object(response)
    # TO-DO: store the processed data in DynamoDB
    return 'Not yet implemented'


def _get_import_controller(event, context):
    """Creates and returns the Controller object"""
    user = User.Factory().load_by_session(context['session_id'])
    return OrganizationImport.Controller(user)
