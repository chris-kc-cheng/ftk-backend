from mongoengine import Document, fields

class Fund(Document):
    name = fields.StringField(required=True, unique=True)
    asset_class = fields.ListField(fields.StringField())