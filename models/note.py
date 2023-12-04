import datetime
from mongoengine import Document, fields
from .user import User
from .fund import Fund

class Note(Document):
    authorId = fields.ReferenceField(User)
    authorName = fields.StringField(required=True)
    fundId = fields.ReferenceField(Fund)
    fundName = fields.StringField(required=True)
    modifiedDate = fields.DateTimeField(default=datetime.datetime.now)
    content = fields.StringField(required=True)
    published = fields.BooleanField(default=False)
    # Meeting date, participants