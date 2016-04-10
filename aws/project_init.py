#!/usr/bin/python
"""
This initializes the project entirely within an AWS account.

Sufficient permissions are needed for this to work.
"""
import boto3
import botocore


# Get the service resource.
DYNAMODB = boto3.resource('dynamodb')


def create_users_table():
    """ Create the 'Users' DynamoDB table """

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


def create_youth_table():
    """ Create the 'Youth' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Youth',
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
    """ Create the 'Volunteers' DynamoDB table """

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
    """ Create the 'Guardians' DynamoDB table """

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


def create_districts_table():
    """ Create the 'Districts' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Districts',
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
                    'AttributeName': 'number',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'district_number',
                    'KeySchema': [
                        {
                            'AttributeName': 'number',
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


def create_subdistricts_table():
    """ Create the 'Subdistricts' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Subdistricts',
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
                    'AttributeName': 'district_id',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'number',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'district_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'district_id',
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
                    'IndexName': 'subdistrict_number',
                    'KeySchema': [
                        {
                            'AttributeName': 'number',
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


def create_sponsoring_orgs_table():
    """ Create the 'SponsoringOrganizations' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='SponsoringOrganizations',
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
                    'AttributeName': 'subdistrict_id',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'subdistrict_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'subdistrict_id',
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


def create_units_table():
    """ Create the 'Units' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='Units',
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
                    'AttributeName': 'sponsoring_organization_id',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'number',
                    'AttributeType': 'N',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'sponsoring_organization_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'sponsoring_organization_id',
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
                    'IndexName': 'unit_number',
                    'KeySchema': [
                        {
                            'AttributeName': 'number',
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


def create_youth_apps_table():
    """ Create the 'YouthApplications' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='YouthApplications',
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
                    'AttributeName': 'unit_id',
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


def create_adult_apps_table():
    """ Create the 'AdultApplications' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='AdultApplications',
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
                    'AttributeName': 'org_id',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'status',
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
                    'IndexName': 'org_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'org_id',
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


def create_charter_apps_table():
    """ Create the 'CharterApplications' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='CharterApplications',
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
                    'AttributeName': 'sponsoring_organization_id',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'status',
                    'AttributeType': 'S',
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'sponsoring_organization_id',
                    'KeySchema': [
                        {
                            'AttributeName': 'sponsoring_organization_id',
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
                    'IndexName': 'year',
                    'KeySchema': [
                        {
                            'AttributeName': 'year',
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


def create_record_log_table():
    """ Create the 'RecordLog' DynamoDB table """

    # Create the DynamoDB table.
    try:
        table = DYNAMODB.create_table(
            TableName='RecordLog',
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
    """ Wait for AWS to finish the table creation process """
    for table_name, table in tables.items():
        if table:
            print "Waiting for '{}' table to finish being created...".format(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print "Done!"


def main():
    """ main """

    # DynamoDB
    tables = {}
    tables['Users'] = create_users_table()
    tables['Youth'] = create_youth_table()
    tables['Volunteers'] = create_volunteers_table()
    tables['Guardians'] = create_guardians_table()
    tables['Districts'] = create_districts_table()
    wait(tables)

    tables = {}
    tables['Subdistricts'] = create_subdistricts_table()
    tables['SponsoringOrganizations'] = create_sponsoring_orgs_table()
    tables['Units'] = create_units_table()
    tables['YouthApplications'] = create_youth_apps_table()
    tables['AdultApplications'] = create_adult_apps_table()
    wait(tables)

    tables = {}
    tables['CharterApplications'] = create_charter_apps_table()
    tables['RecordLog'] = create_record_log_table()
    wait(tables)

    # API Gateway

    # S3 Buckets

    # S3 Static Web Site

    # Lambda


if __name__ == '__main__':
    main()
