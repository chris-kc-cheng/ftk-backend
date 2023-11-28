import os, secrets
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_session import Session
import flask_praetorian
import toolkit as ftk
from models import User, Note

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['MONGODB_SETTINGS'] = {'db': 'ftk-db'}
app.config['SECRET_KEY'] = secrets.token_urlsafe() # os.getenv('SECRET_KEY')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

guard = flask_praetorian.Praetorian()

db = MongoEngine(app)
guard.init_app(app, User)
sess = Session(app)
CORS(app)

@app.route('/')
def index():
    return '<p>Financial Toolkit</p>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Return JSON Web Token upon successful login

    Returns
    -------
    Successful:
    {
        "access_token": "..."
    }

    Otherwise:
    {
        "error": "AuthenticationError",
        "message": "The username and/or password are incorrect",
        "status_code": 401
    }
    """
    username = request.args.get('username')
    password = request.args.get('password')
    user = guard.authenticate(username, password)
    return jsonify(access_token=guard.encode_jwt_token(user))

@app.route('/protected', methods=['GET', 'POST'])
@flask_praetorian.auth_required
def protected():
    return flask_praetorian.current_user().username

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

@app.route('/notes/new', methods=['POST'])
def add_notes():
    content = request.json['content']
    note = Note(content=content).save()
    return jsonify({'id': str(note.id)})

@app.route('/notes/all')
def get_notes():
    return jsonify(Note.objects)