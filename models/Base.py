""" Base classes """
import boto3
import shortuuid


FIELD_REQUIRED = 'required'
FIELD_OPTIONAL = 'optional'


class Object(object):

    """ Base class """

    def __init__(self, init_data=None):
        if init_data:
            for key, _ in self.__class__.get_fields().items():
                if key in init_data:
                    self.__dict__[key] = init_data[key]
        if not hasattr(self, 'uuid'):
            self.uuid = self.__class__.get_uuid_prefix()+'-'+shortuuid.uuid()

    @staticmethod
    def get_uuid_prefix():
        """ Must be defined by the child class """
        raise Exception('SYSTEM ERROR: prefix not defined.')

    @staticmethod
    def get_fields():
        """ Must be defined by the child class """
        raise Exception('SYSTEM ERROR: field structure not defined.')

    def valid(self):
        """ Determine validity of the object """
        valid = True

        for key, value in self.get_fields().items():
            if value == FIELD_REQUIRED:
                if key not in self.__dict__:
                    valid = False
                    break

        return valid


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
        if obj.valid():
            self.table.put_item(Item=obj.__dict__)
        else:
            raise Exception("Error saving.")

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
