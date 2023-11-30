from flask_mongoengine import MongoEngine
import flask_praetorian

db = MongoEngine()
guard = flask_praetorian.Praetorian()