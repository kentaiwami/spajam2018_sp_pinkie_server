from flask import Blueprint, jsonify, request
from model import User, Walk
from database import session
from jsonschema import validate, ValidationError


app = Blueprint('start_bp', __name__)

@app.route('/api/walk', methods=['POST'])
def post():
    schema = {'type': 'object',
              'properties':
                  {'user_id': {'type': 'integer', 'minimum': 0}},
              'required': ['user_id']
              }

    try:
        validate(request.json, schema)
    except ValidationError as e:
        return jsonify({'msg': e.message}), 400

    user = session.query(User).filter(User.id == request.json['user_id']).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    walk = Walk(user_id=user.id)
    session.add(walk)
    session.commit()
    session.close()

    return jsonify({'walk_id': walk.id}), 200
