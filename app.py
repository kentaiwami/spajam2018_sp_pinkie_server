from database import init_db
from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from model import db
from config import secret_key
from views import test, pull, start, end
from admin import AuthException, init_admin


def init_app():
    app_obj = Flask(__name__)
    app_obj.config.from_object('config.BaseConfig')
    app_obj.secret_key = secret_key

    init_db(app_obj)
    init_admin(app_obj)
    add_bp(app_obj)

    return app_obj


def add_bp(app_obj):
    modules_define = [
        test.app, pull.app, start.app, end.app
    ]

    for bp_app in modules_define:
        app_obj.register_blueprint(bp_app)


app = init_app()
admin_basic_auth = BasicAuth(app)
migrate = Migrate(app, db)


@app.route('/logout')
def Logout():
    raise AuthException('Successfully logged out.')


@app.route('/')
@app.route('/index')
def index():
    return 'This is index page'
