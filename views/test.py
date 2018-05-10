from flask import Blueprint, jsonify
from model import User
from database import session

app = Blueprint('test_bp', __name__)


@app.route('/api/hello', methods=['GET'])
def hello():
    user = session.query(User).all()

    return "Hello World! " + str(len(user))
