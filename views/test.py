from flask import Blueprint, jsonify
from model import User
from database import session

app = Blueprint('test_bp', __name__)


@app.route('/api/hello', methods=['GET'])
def hello():
    user = session.query(User).all()

    return jsonify({'msg': 'Hello World', 'count': len(user)}), 200
