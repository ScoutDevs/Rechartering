#!/usr/bin/python

# test stuff out
import boto3
import shortuuid


def testUsersTable():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    table.put_item(Item=getUser('ben'))
    table.put_item(Item=getUser('ken'))
    table.put_item(Item=getUser('callie'))


def getUser(username):
    return {
        'id': shortuuid.uuid(),
        'username': username,
        'password': 'password',
        'roles': [
            {
                'type': 'district',
                'id': '123',
                'role': 'admin',
            },
        ],
    }

if __name__ == '__main__':
    testUsersTable()
