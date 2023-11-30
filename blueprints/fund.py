from flask import Blueprint, request, jsonify
import flask_praetorian

bp_fund = Blueprint('fund', __name__)

@bp_fund.route('/add', methods=['POST'])
@flask_praetorian.auth_required
def add():
    a = int(request.json['a'])
    b = int(request.json['b'])
    return jsonify({'sum': a + b})
