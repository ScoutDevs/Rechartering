#!/usr/bin/python
"""
This initializes the project entirely within an AWS account.

Sufficient permissions are needed for this to work.
"""
from __future__ import print_function

import boto3
import botocore

# Get the service resource.
DYNAMODB = boto3.resource('dynamodb')


def create_users_table():
    """Create the 'Users' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'password',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'session_uuid',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'username',
                    'KeySchema': [
                        {
                            'AttributeName': 'username',
                            'KeyType': 'HASH',
                        },
                        {
                            'AttributeName': 'password',
                            'KeyType': 'RANGE',
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'session_uuid',
                    'KeySchema': [
                        {
                            'AttributeName': 'session_uuid',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_people_table():
    """Create the 'People' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='People',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'duplicate_hash',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'scoutnet_id',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'organization_uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'user_uuid',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'duplicate_hash',
                    'KeySchema': [
                        {
                            'AttributeName': 'duplicate_hash',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'scoutnet_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'scoutnet_id',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'organization_uuid',
                    'KeySchema': [
                        {
                            'AttributeName': 'organization_uuid',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'user_uuid',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_uuid',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_volunteers_table():
    """Create the 'Volunteer' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Volunteers',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'duplicate_hash',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'scoutnet_id',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'unit_id',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'duplicate_hash',
                    'KeySchema': [
                        {
                            'AttributeName': 'duplicate_hash',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'scoutnet_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'scoutnet_id',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'unit_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'unit_id',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_guardians_table():
    """Create the 'Guardian' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Guardians',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_organizations_table():
    """Create the 'Organization' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Organizations',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'parent_uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'number',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'type',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'parent_uuid',
                    'KeySchema': [
                        {
                            'AttributeName': 'parent_uuid',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10,
                    },
                },
                {
                    'IndexName': 'number',
                    'KeySchema': [
                        {
                            'AttributeName': 'number',
                            'KeyType': 'HASH',
                        },
                        {
                            'AttributeName': 'type',
                            'KeyType': 'RANGE',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_applications_table():
    """Create the 'Applications' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Applications',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'status',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'organization_uuid',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'status',
                    'KeySchema': [
                        {
                            'AttributeName': 'status',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
                {
                    'IndexName': 'organization_uuid',
                    'KeySchema': [
                        {
                            'AttributeName': 'organization_uuid',
                            'KeyType': 'HASH',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def create_record_logs_table():
    """Create the 'RecordLogs' DynamoDB table"""

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='RecordLogs',
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        return table
    except botocore.exceptions.ClientError as exc:
        if 'ResourceInUseException' not in exc.__str__():
            raise exc


def wait(tables):
    """Wait for AWS to finish the table creation process"""
    for table_name, table in tables.items():
        if table:
            print("Waiting for '{}' table to finish being created...".format(table_name))
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print("Done!")


def main():
    """main"""

    # DynamoDB
    tables = {}
    tables['Users'] = create_users_table()
    tables['People'] = create_people_table()
    tables['Organizations'] = create_organizations_table()
    tables['Applications'] = create_applications_table()
    tables['RecordLogs'] = create_record_logs_table()
    wait(tables)

    # API Gateway

    # S3 Buckets
    #   S3 Static Web Site

    # SNS topics

    # Lambda


if __name__ == '__main__':
    main()
