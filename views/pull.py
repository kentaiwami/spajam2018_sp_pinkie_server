from flask import Blueprint, jsonify, request
from model import User, Pull
from database import session

app = Blueprint('pull_bp', __name__)


@app.route('/api/pull', methods=['GET'])
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
