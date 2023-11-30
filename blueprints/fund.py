from flask import Blueprint, request, jsonify
import flask_praetorian
from extensions import db
from models.fund import Fund

bp_fund = Blueprint('fund', __name__)

@bp_fund.route('/add', methods=['POST'])
@flask_praetorian.auth_required
def add():
    a = int(request.json['a'])
    b = int(request.json['b'])
    return jsonify({'sum': a + b})

@bp_fund.route('/create', methods=['POST'])
@flask_praetorian.auth_required
def create():
    req = request.get_json(force=True)
    name = req.get('fundName', None)    
    return jsonify({'sum': 123})

@bp_fund.route('/all')
@flask_praetorian.auth_required
def all():
    return jsonify(Fund.objects.only('name').order_by('name')), 200