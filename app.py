import os, secrets

from flask import Flask
from flask_cors import CORS
import toolkit as ftk

from extensions import db, guard
from models import User
from blueprints.user import bp_user
from blueprints.fund import bp_fund
from blueprints.note import bp_note
from blueprints.admin import bp_admin
from blueprints.performance import bp_performance

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST')

# React client has to re-login upon each server restart
# app.config['SECRET_KEY'] = secrets.token_urlsafe()

# For development only
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# Extensions
db.init_app(app)
guard.init_app(app, User)

CORS(app)

# Blueprints
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_fund, url_prefix='/fund')
app.register_blueprint(bp_note, url_prefix='/note')
app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_performance, url_prefix='/performance')

@app.route('/')
def index():
    return '<h1>FTK Backend is up and running</h1>'
