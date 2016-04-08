""" Base classes """
import boto3
import shortuuid


FIELD_REQUIRED = 'required'
FIELD_OPTIONAL = 'optional'


class Object(object):

    """ Base class """

    def __init__(self, init_data=None):
        if init_data:
            for key, _ in self.get_validator().get_field_requirements().items():
                if key in init_data:
                    self.__dict__[key] = init_data[key]
        if not hasattr(self, 'uuid'):
            self.uuid = self.__class__.get_uuid_prefix()+'-'+shortuuid.uuid()

    @staticmethod
    def get_uuid_prefix():
        """
        UUID prefix to easily identify record types

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: prefix not defined.')

    def prepare_for_persist(self):
        """
        Called by the persister prior to validation & storage

        Useful for setting derived values.
        """
        pass

    def get_validator(self):  # pylint: disable=no-self-use
        """
        Returns a Validator object for validation

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: validator not defined.')


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

    @staticmethod
    def get_field_types():
        """
        Specify the data types for fields for validation.

        Must be defined by the child class.
        """
        raise Exception('SYSTEM ERROR: field structure not defined.')

    def _validate_required_fields(self):
        """ Validate that the data provided includes all required fields """
        valid = True
        errors = []

        for key, value in self.get_field_requirements().items():
            if value == FIELD_REQUIRED:
                if key not in self.obj.__dict__:
                    errors.append("Missing required field {}".format(key))
                    valid = False

        return (valid, errors)

    def _validate_field_types(self):
        """ Validate that the data provided matches the expected types """
        valid = True
        errors = []

        for field, data_type in self.get_field_types().items():
            if field not in self.obj.__dict__:  # field requirements handled elsewhere
                continue
            if not isinstance(self.obj.__dict__[field], data_type):
                errors.append('Invalid data type {}; expected {}, got [{}]'.format(
                    type(self.obj.__dict__[field]),
                    data_type,
                    self.obj.__dict__[field]))
                valid = False

        return (valid, errors)

    def _validate(self):  # pylint: disable=no-self-use
        """ Any additional validation can be done in this method in the child """
        return (True, [])

    def valid(self):
        """ Determine validity of the object """
        (requirements_valid, _) = self._validate_required_fields()
        (field_types_valid, _) = self._validate_field_types()
        (other_valid, _) = self._validate()
        return requirements_valid and field_types_valid and other_valid

    def get_validation_errors(self):
        """ Provide errors associated with validation """
        (_, requirements_errors) = self._validate_required_fields()
        (_, field_types_errors) = self._validate_field_types()
        (_, other_errors) = self._validate()
        return requirements_errors + field_types_errors + other_errors


class Factory(object):

    """ Base Factory """

    def __init__(self):
        self.persister = self._get_persister()  # pylint: disable=assignment-from-no-return

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
        obj = klass(data)
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
        obj.prepare_for_persist()
        validator = obj.get_validator()
        if validator.valid():
            self.table.put_item(Item=obj.__dict__)
        else:
            raise InvalidObjectException("Error saving data to {}.".format(self._get_table_name()))

    def get(self, key):
        """ Load from DB """
        item = self.table.get_item(Key=key)
        if 'Item' in item:
            return item['Item']
        else:
            raise RecordNotFoundException('Record not found')

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
