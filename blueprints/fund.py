from flask import Blueprint, request, jsonify
import flask_praetorian
from mongoengine.errors import NotUniqueError
from models.fund import Fund

bp_fund = Blueprint('fund', __name__)

@bp_fund.route('/create', methods=['POST'])
@flask_praetorian.auth_required
def create_fund():
    req = request.get_json(force=True)
    print('Creating', req)
    # Frontend sends empty string for name and None for launchDate and empty array for assetClasses
    fundName = req.get('fundName', '')
    firmName = req.get('firmName', '')
    assetClasses = req.get('assetClasses', [])
    launchDate = req.get('launchDate', None)
    if len(fundName) == 0:
        return jsonify({
            'status': 'error',
            'message': 'Fund name cannot be empty'})
    if len(firmName) == 0:
        return jsonify({
            'status': 'error',
            'message': 'Firm name cannot be empty'})
    if len(assetClasses) == 0:
        return jsonify({
            'status': 'error',
            'message': 'At least one asset class must be specified'})
    fund = Fund(name=fundName, firm=firmName, assetClasses=assetClasses, launchDate=launchDate)
    try:
        fund.save()
    except NotUniqueError:
        return jsonify({
            'status': 'error',
            'message': 'Fund name is duplicated'})
    return jsonify({
        'status': 'success',
        'message': f'{fundName} is created',
        'id': str(fund.id)
    })

@bp_fund.route('/')
@flask_praetorian.auth_required
def get_funds():
    """Get list of all funds for autocomplete
    """
    return jsonify(Fund.objects.only('name').order_by('name')), 200

@bp_fund.route('/<id>')
@flask_praetorian.auth_required
def get_fund(id):
    print('Fund detail')
    fund = Fund.objects.get(pk=id)
    ret = {
        'name': fund.name,
        'firm': fund.firm,
        'assetClasses': fund.assetClasses,
        'launchDate': fund.launchDate
    }
    return jsonify(ret), 200
