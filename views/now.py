from flask import Blueprint, jsonify, request
from model import User, Walk, Pull
from database import session
from jsonschema import validate, ValidationError
from sqlalchemy import between
from sqlalchemy import func


app = Blueprint('now_bp', __name__)

@app.route('/api/walk/now', methods=['GET'])
def get():

    if request.args.get('user_id') is None:
        return jsonify({'msg': 'user_idがない!!'}), 400

    user = session.query(User).filter(User.id == request.args.get('user_id')).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    walk = session.query(Walk).order_by(Walk.id.desc()).first()
    now_count = session.query(Pull).filter(between(Pull.created_at, walk.started_at, walk.ended_at)).count()

    return jsonify({'now': now_count}), 200
