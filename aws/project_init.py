#!/usr/bin/python
"""
This initializes the project entirely within an AWS account.

Sufficient permissions are needed for this to work.
"""
import boto3


def create_users_table():
    """ Create the 'Users' DynamoDB table """

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
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


def wait(tables):
    """ Wait for AWS to finish the table creation process """
    for table_name, table in tables.items():
        print "Waiting for '{}' table to finish being created...".format(table_name)
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print "Done!"


def main():
    """ main """

    # DynamoDB
    tables = {}
    tables['Users'] = create_users_table()
    wait(tables)

    # API Gateway

    # S3 Buckets

    # S3 Static Web Site

    # Lambda


if __name__ == '__main__':
    main()
