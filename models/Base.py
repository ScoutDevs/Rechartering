""" Base classes """
from boto3.dynamodb.conditions import Key
import boto3
import shortuuid


FIELD_REQUIRED = 'required'
FIELD_OPTIONAL = 'optional'


class Object(object):

    """ Base class """

    def __init__(self):
        self.uuid = self.get_factory().get_uuid()

    def get_validator(self):  # pylint: disable=no-self-use
        """
        Returns a Validator object for validation

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: validator not defined.')

    @staticmethod
    def get_factory():
        """
        Returns a Factory object

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: factory not defined.')

    def validate(self):
        """ Validate the object """
        return self.get_validator().validate()


class Validator(object):

    """ Validates data construct """

    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def get_field_requirements():
        """
        Specify which fields are used, and whether they're required

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: field requirements not defined.')

    def _validate_required_fields(self):
        """ Validate that the data provided includes all required fields """
        valid = True
        errors = []

        for key, value in self.get_field_requirements().items():
            if value == FIELD_REQUIRED:
                if key not in self.obj.__dict__ or not self.obj.__dict__[key]:
                    errors.append("Missing required field {}".format(key))
                    valid = False

        return (valid, errors)

    def prepare_for_validate(self):
        """
        Called by the persister prior to validation & storage

        Useful for setting derived values.
        """
        pass

    def _validate(self):  # pylint: disable=no-self-use
        """ Any additional validation can be done in this method in the child """
        return (True, [])

    def valid(self):
        """ Determine validity of the object """
        self.prepare_for_validate()
        (requirements_valid, _) = self._validate_required_fields()
        (other_valid, _) = self._validate()
        return requirements_valid and other_valid

    def validate(self):
        """ Validates the object """
        errors = self.get_validation_errors()
        if errors:
            # if sys.stdin.isatty() print errors
            raise InvalidObjectException(errors[0])

    def get_validation_errors(self):
        """ Provide errors associated with validation """
        self.prepare_for_validate()
        (_, requirements_errors) = self._validate_required_fields()
        (_, other_errors) = self._validate()
        return requirements_errors + other_errors


class Factory(object):

    """ Base Factory """

    def __init__(self):
        self.persister = self._get_persister()  # pylint: disable=assignment-from-no-return

    @staticmethod
    def _get_uuid_prefix():
        """
        UUID prefix to easily identify record types

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: prefix not defined.')

    def get_uuid(self):
        """ Generates a UUID """
        return "{}-{}".format(self._get_uuid_prefix(), shortuuid.uuid())

    def load_by_uuid(self, uuid):
        """ Load by UUID """
        return self.load_from_database({'uuid': uuid})

    def load_from_database(self, search_data):
        """ Load from DB """
        item_data = self.persister.get(search_data)
        return self.construct(item_data)

    def construct(self, data):
        """ Create object from dict """
        klass = self._get_object_class()  # pylint: disable=assignment-from-no-return
        obj = klass()
        for key, _ in obj.__dict__.items():
            if key in data:
                obj.__dict__[key] = data[key]
        return obj

    @staticmethod
    def _get_persister():
        raise Exception('SYSTEM ERROR: persister not defined.')

    @staticmethod
    def _get_object_class():
        raise Exception('SYSTEM ERROR: class not defined.')


class Persister(object):

    """ Persists objects """

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(self._get_table_name())

    def save(self, obj):
        """ Save to DB """
        obj.get_validator().validate()
        persist_obj = self.__class__.get_persistable_object(obj)
        self.table.put_item(Item=persist_obj)

    @staticmethod
    def get_persistable_object(obj):
        """
        Give DynamoDB what it wants

        DynamoDB wants a dict, not an object
        DynamoDB won't store empty fields, so get rid of 'em
        """
        new_dict = {}
        for key, val in obj.__dict__.items():
            if val != '':
                new_dict[key] = val
        return new_dict

    def get(self, key):
        """ Load from DB """
        item = self.table.get_item(Key=key)
        if 'Item' in item:
            return item['Item']
        else:
            raise RecordNotFoundException('Record not found')

    def query(self, key, value):
        """ Search DB with index and return 0 or more records """
        result = self.table.query(
            IndexName=key,
            KeyConditionExpression=Key(key).eq(value)
        )

        if 'Items' in result:
            items = result['Items']
        else:
            raise Exception('Error searching')

        return items

    def delete(self, obj):
        """ Delete from DB """
        self.table.delete_item(Key={'uuid': obj.uuid})

    @staticmethod
    def _get_table_name():
        """ Must be implemented by child class. """
        raise Exception('SYSTEM ERROR: No table name specified.')


class RecordNotFoundException(Exception):
    """ Record not found """
    pass


class InvalidObjectException(Exception):
    """ Object is not in valid state """
    pass
