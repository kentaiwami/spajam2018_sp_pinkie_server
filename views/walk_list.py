from flask import Blueprint, jsonify, request
from model import User, Walk, Pull
from database import session
from jsonschema import validate, ValidationError
from sqlalchemy import between
from sqlalchemy import func


app = Blueprint('walk_list_bp', __name__)

@app.route('/api/walk/list', methods=['GET'])
def get():

    if request.args.get('user_id') is None:
        return jsonify({'msg': 'user_idがない!!'}), 400

    user = session.query(User).filter(User.id == request.args.get('user_id')).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    walks = session.query(Walk).filter(Walk.user_id == user.id).all()

    results = []
    for walk in walks:
        pull = session.query(Pull).filter(between(Pull.created_at, walk.started_at, walk.ended_at)).count()

        results.append({'count': pull, 'date': '{0:%Y-%m-%d}'.format(walk.started_at), 'id': walk.id})


    return jsonify({'results': results}), 200
