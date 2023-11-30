from flask import Blueprint, request, jsonify
import flask_praetorian
from extensions import guard

bp_user = Blueprint('user', __name__)

@bp_user.route('/login', methods=['POST'])
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
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    #user.lastLogin = ...
    json = jsonify(access_token=guard.encode_jwt_token(user))
    return json, 200

@bp_user.route('/refresh', methods=['POST'])
def refresh():
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200

@bp_user.route('/reset', methods=['POST'])
@flask_praetorian.auth_required
def reset_password():
    user = flask_praetorian.current_user()
    print('Reset password for', user)
    req = request.get_json(force=True)
    old_password = req.get('old_password', None)
    new_password = req.get('new_password', None)
    confirm_password = req.get('confirm_password', None)
    guard.authenticate(user.username, old_password)
    return {}, 200

@bp_user.route('/profile', methods=['GET'])
@flask_praetorian.auth_required
def profile():
    user = flask_praetorian.current_user()
    ret = {
        'username': user.username,
        'first_name': user.firstName,
        'last_name': user.lastName,
        'is_active': user.isActive,
        'roles': user.rolenames,
        #'last_login': user.lastLogin
    }
    return ret, 200