from flask import Blueprint, jsonify, request
from model import User, Pull
from database import session
from jsonschema import validate, ValidationError


app = Blueprint('pull_bp', __name__)


@app.route('/api/pull/test', methods=['GET'])
# getだけど強制登録
def get():
    user = session.query(User).filter(User.id == 1).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    pull = Pull(user_id=user.id)
    session.add(pull)
    session.commit()
    session.close()

    return jsonify({'msg': 'Success'}), 200


@app.route('/api/pull', methods=['POST'])
def post():
    schema = {'type': 'object',
              'properties':
                  {'id': {'type': 'integer', 'minimum': 0}},
              'required': ['id']
              }

    try:
        validate(request.json, schema)
    except ValidationError as e:
        return jsonify({'msg': e.message}), 400

    user = session.query(User).filter(User.id == request.json['id']).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    pull = Pull(user_id=user.id)
    session.add(pull)
    session.commit()
    session.close()

    return jsonify({'id': request.json['id']}), 200
