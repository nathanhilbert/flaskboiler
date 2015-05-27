# coding=utf-8
from json import dumps, loads
from sqlalchemy.types import Text, TypeDecorator, Integer
from sqlalchemy.schema import Table, Column
from sqlalchemy.sql.expression import and_, select, func
from sqlalchemy.ext.mutable import Mutable

from flaskboiler.core import db

ALIAS_PLACEHOLDER = u'‽'

class MutableDict(Mutable, dict):

    """
    Create a mutable dictionary to track mutable values
    and notify listeners upon change.
    """

    @classmethod
    def coerce(cls, key, value):
        """
        Convert plain dictionaries to MutableDict
        """

        # If it isn't a MutableDict already we conver it
        if not isinstance(value, MutableDict):
            # If it is a dictionary we can convert it
            if isinstance(value, dict):
                return MutableDict(value)
            elif isinstance(value, unicode):
                print value
                newval = loads(value)
                return MutableDict(newval)

            # Try to coerce but it will probably return a ValueError
            return Mutable.coerce(key, value)
        else:
            # Since we already have a MutableDict we can just return it
            return value

    def __setitem__(self, key, value):
        """
        Set a value to a key and notify listeners of change
        """

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """
        Delete a key and notify listeners of change
        """

        dict.__delitem__(self, key)
        self.changed()


class JSONType(TypeDecorator):
    impl = Text

    def __init__(self):
        super(JSONType, self).__init__()

    def process_bind_param(self, value, dialect):
        return dumps(value)

    def process_result_value(self, value, dialiect):
        return loads(value)

    def copy_value(self, value):
        return loads(dumps(value))

