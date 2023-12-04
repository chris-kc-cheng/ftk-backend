import os, secrets

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import flask_praetorian
import toolkit as ftk
from flask_session import Session

from extensions import db, guard
from models import User
from blueprints.user import bp_user
from blueprints.fund import bp_fund
from blueprints.note import bp_note

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

sess = Session(app)
CORS(app)

# Blueprints
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_fund, url_prefix='/fund')
app.register_blueprint(bp_note, url_prefix='/note')

@app.route('/')
def index():
    return '<h1>FTK Backend</h1>'

@app.route('/debug')
@flask_praetorian.roles_required("admin")
def debug():
    return dict(os.environ.items())

@app.route('/counter')
def counter():
    session['counter'] = session.get('counter', 0) + 1
    return f'Visited {session["counter"]}'

@app.route('/ticker/<ticker>')
def get_price(ticker):
    return ftk.get_yahoo(ticker).to_json()
