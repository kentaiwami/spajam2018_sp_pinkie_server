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

    # return jsonify({'hoge': request.json['walk_id']}), 200
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

    user_id = walk.user_id

    sql = 'select from_unixtime(round(unix_timestamp(created_at) div(5 * 60)) *(5 * 60)) as timekey, count(*) from pull, walk where pull.user_id = %s and pull.created_at BETWEEN (SELECT started_at FROM `walk` WHERE user_id = %s order by started_at desc LIMIT 1) and (SELECT ended_at FROM `walk` WHERE user_id = %s order by ended_at desc LIMIT 1) group by timekey;' % (user_id, user_id, user_id)
    sql_res = session.execute(sql)

    results = []

    for res in sql_res:
        results.append({'time': str(res[0]), 'count': res[1]})

    return jsonify({'results': results}), 200
