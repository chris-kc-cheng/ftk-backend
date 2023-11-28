from bson.json_util import loads, dumps
from mongoengine import Document, fields, DoesNotExist

class User(Document):
    username = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
    roles = fields.StringField()
    is_active = fields.BooleanField(default=True)

    @classmethod
    def lookup(cls, username):
        try:
            return User.objects(username=username).get()
        except DoesNotExist:
            return None

    @classmethod
    def identify(cls, id):
        try:
            return User.objects(id=loads(id)).get()
        except DoesNotExist:
            return None

    @property
    def rolenames(self):
        return []

    @property
    def identity(self):
        return dumps(self.id)

    def is_valid(self):
        return self.is_active