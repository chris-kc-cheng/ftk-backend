import datetime
from mongoengine import Document, fields

class Note(Document):
    modified_date = fields.DateTimeField(default=datetime.datetime.now)
    content = fields.StringField(required=True)