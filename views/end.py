from datetime import datetime
from flask import Blueprint, jsonify, request
from model import Walk
from database import session
from jsonschema import validate, ValidationError


app = Blueprint('end_bp', __name__)


@app.route('/api/walk', methods=['PUT'])
def put():
    schema = {'type': 'object',
              'properties':
                  {'walk_id': {'type': 'integer', 'minimum': 0}},
              'required': ['walk_id']
              }

    try:
        validate(request.json, schema)
    except ValidationError as e:
        return jsonify({'msg': e.message}), 400

    walk = session.query(Walk).filter(Walk.id == request.json['walk_id']).one_or_none()

    if walk is None:
        return jsonify({'msg': 'Walk Not Found'}), 404

    walk.ended_at = datetime.now()
    session.commit()
    session.close()

    return jsonify({'msg': 'Success'}), 200
