from flask import Blueprint, request, jsonify
import flask_praetorian
from mongoengine.errors import NotUniqueError
from models.fund import Fund
from models.note import Note

bp_note = Blueprint('note', __name__)

@bp_note.route('/create', methods=['POST'])
@flask_praetorian.auth_required
def create():
    # author, fund, modifiedDate, content, published
    user = flask_praetorian.current_user()
    req = request.get_json(force=True)
    print('Creating Note', req)
    # Frontend sends empty string for name and None for launchDate and empty array for assetClasses
    fundId = req.get('fundId', '')
    note = Note(author=user, fund=Fund.objects.get(pk=fundId), content='', published=False)
    return {'id': str(note.id)}