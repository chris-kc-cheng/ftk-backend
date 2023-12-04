from flask import Blueprint, request, jsonify
import flask_praetorian
import json
from bson import json_util
from bson.objectid import ObjectId
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
    fund = Fund(name=fundName, firm=firmName,
                assetClasses=assetClasses, launchDate=launchDate)
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
    print('Fund Details')
    fund = Fund.objects.get(pk=id)
    return jsonify(fund), 200


@bp_fund.route('/<id>/note')
@flask_praetorian.auth_required
def get_fund_notes(id):
    print('Fund Notes')
    notes = Fund.objects.aggregate([
        {
            '$match': {
                '_id': ObjectId(id)
            }
        }, {
            '$lookup': {
                'from': 'note',
                'localField': '_id',
                'foreignField': 'fund',
                'as': 'notes'
            }
        }, {
            '$unwind': {
                'path': '$notes'
            }
        }, {
            '$lookup': {
                'from': 'user',
                'localField': 'notes.author',
                'foreignField': '_id',
                'as': 'authors'
            }
        }, {
            '$unwind': {
                'path': '$authors'
            }
        }, {
            '$addFields': {
                'notes': {
                    'authorName': {
                        '$concat': [
                            '$authors.firstName', ' ', '$authors.lastName'
                        ]
                    }
                }
            }
        }, {
            '$project': {
                'fundId': '$notes.fund',
                'authorId': '$notes.author',
                'authorName': '$notes.authorName',
                'noteId': '$notes._id',
                'modifiedDate': '$notes.modifiedDate',
                'content': '$notes.content',
                'published': '$notes.published'
            }
        }
    ])
    ret = json.loads(json_util.dumps(notes))
    return jsonify(ret), 200
