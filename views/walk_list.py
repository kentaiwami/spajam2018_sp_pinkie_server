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

    walks = session.query(Walk).filter(Walk.user_id == user.id).order_by(Walk.started_at.desc())

    results = []
    for walk in walks:
        pull = session.query(Pull).filter(between(Pull.created_at, walk.started_at, walk.ended_at)).count()

        results.append({'count': str(pull), 'date': '{0:%Y-%m-%d}'.format(walk.started_at), 'id': walk.id})


    return jsonify({'results': results}), 200


@app.route('/api/walk/list/<id>', methods=['GET'])
def get_detail(id):
    if request.args.get('user_id') is None:
        return jsonify({'msg': 'user_idがない!!'}), 400

    user = session.query(User).filter(User.id == request.args.get('user_id')).one_or_none()

    if user is None:
        return jsonify({'msg': 'User Not Found'}), 404

    walk = session.query(Walk).filter(Walk.id == id).one_or_none()

    if walk is None:
        return jsonify({'msg': 'Walk Not Found'}), 404

    sql = 'select from_unixtime(round(unix_timestamp(created_at) div(5 * 60)) *(5 * 60)) as timekey, count(*) from pull, walk where pull.user_id = %s and pull.created_at BETWEEN (SELECT started_at FROM `walk` WHERE user_id = %s AND id = %s) and (SELECT ended_at FROM `walk` WHERE user_id = %s AND id = %s) group by timekey;' % (user.id, user.id, walk.id, user.id, walk.id)
    sql_res = session.execute(sql)

    results = []

    for res in sql_res:
        results.append({'time': '{0:%H:%M}'.format(res[0]), 'count': int(res[1] / 10)})

    return jsonify({'results': results}), 200
