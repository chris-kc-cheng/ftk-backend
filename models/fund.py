from mongoengine import Document, fields

class Fund(Document):
    name = fields.StringField(required=True, unique=True)
    firm = fields.StringField(required=True)
    assetClasses = fields.ListField(fields.StringField())    
    launchDate = fields.DateField()
    #portfolioManagers = fields.ListField(fields.StringField())
