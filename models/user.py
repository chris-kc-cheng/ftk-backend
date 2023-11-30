from bson.json_util import loads, dumps
from mongoengine import Document, fields, DoesNotExist

class User(Document):
    username = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
    firstName = fields.StringField(required=True)
    lastName = fields.StringField(required=True)
    isActive = fields.BooleanField(default=True)
    #lastLogin = fields.DateTimeField()
    roles = fields.ListField(fields.StringField())

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
        return self.roles

    @property
    def identity(self):
        return dumps(self.id)

    def is_valid(self):
        return self.isActive