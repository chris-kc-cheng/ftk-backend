import datetime
from mongoengine import Document, fields
from .user import User
from .fund import Fund

class Note(Document):
    author = fields.ReferenceField(User)
    fund = fields.ReferenceField(Fund)
    modifiedDate = fields.DateTimeField(default=datetime.datetime.now)
    content = fields.StringField(required=True)
    published = fields.BooleanField(default=False)
    # Meeting date, participants