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
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2,
            }
        )
        return table
    except botocore.exceptions.ClientError:
        pass


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
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2,
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
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2,
                    },
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2,
            }
        )
        return table
    except botocore.exceptions.ClientError:
        pass


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
    wait(tables)

    # API Gateway

    # S3 Buckets

    # S3 Static Web Site

    # Lambda


if __name__ == '__main__':
    main()
