import os, secrets
from flask import Blueprint, request, jsonify
import flask_praetorian
from extensions import guard
from models.user import User

bp_admin = Blueprint('admin', __name__)


@bp_admin.route('/user', methods=['POST'])
@flask_praetorian.roles_required("admin")
def create_user():
    req = request.get_json(force=True)
    username = req.get('username', '')
    password = req.get('password', secrets.token_urlsafe())
    firstName = req.get('firstName', '')
    lastName = req.get('lastName', '')
    isActive = req.get('isActive', True)
    roles = req.get('roles', ['user'])
    user = User(username=username, password=guard.hash_password(
        password), firstName=firstName, lastName=lastName, isActive=isActive, roles=roles)
    user.save()
    return {}, 200


@bp_admin.route('/debug')
@flask_praetorian.roles_required("admin")
def debug():
    return dict(os.environ.items())
