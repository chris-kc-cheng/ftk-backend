import datetime
from bson import json_util
from flask import Blueprint, request, jsonify
import flask_praetorian
from models.fund import Fund
from models.note import Note

bp_note = Blueprint('note', __name__)

@bp_note.route('/')
@flask_praetorian.auth_required
def get_notes():
    skip = int(request.args.get('skip', default=0))
    limit = int(request.args.get('limit', default=10))
    return jsonify(Note.objects[skip:skip+limit])

@bp_note.route('/', methods=['POST'])
@flask_praetorian.auth_required
def create():
    # author, fund, modifiedDate, content, published
    user = flask_praetorian.current_user()
    req = request.get_json(force=True)
    print('Creating Note', req)
    # Frontend sends empty string for name and None for launchDate and empty array for assetClasses
    fundId = req.get('fundId', '')
    fund = Fund.objects.get(pk=fundId)
    print(fund.id)
    note = Note(
        authorId=user,
        authorName=user.firstName + ' ' + user.lastName,
        fundId=fund,
        fundName=fund.name,
        content='',
        published=False)
    note.save()
    print('Creating note', str(note.id))
    return {'id': str(note.id)}

@bp_note.route('/<id>')
@flask_praetorian.auth_required
def get_note(id):
    note = Note.objects.get(pk=id)
    ret = {
        'fundName': note.fundName,
        'content': note.content,
        'published': note.published
    }
    print('Detail', ret)
    return jsonify(ret), 200


@bp_note.route('/<id>', methods=['PUT'])
@flask_praetorian.auth_required
def put_note(id):
    # TODO: Check user is the original author
    user = flask_praetorian.current_user()
    req = request.get_json(force=True)
    note = Note.objects.get(pk=id)
    note.content = req.get('content', '')
    note.published = req.get('published', False)
    note.modifiedDate = datetime.datetime.now
    note.save()
    return jsonify({
        'status': 'success'
    }), 200
