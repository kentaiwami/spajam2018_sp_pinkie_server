from database import init_db, session
from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from model import db, Pull, Walk
from config import secret_key
from views import pull, start, end, now, prev_walk, walk_list
from admin import AuthException, init_admin
import random
from datetime import datetime
# import datetime
from datetime import timedelta


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
        pull.app, start.app, end.app, now.app, prev_walk.app, walk_list.app
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




@app.cli.command()
def insertdd():
    # walkをinsert
    # for i in range(1, 13):
        # hour = random.randint(8, 17)
        # miniute = random.randint(0, 59)
        # start_walk_datetime = datetime(2018, 5, i, hour, miniute, 0)
        # end_walk_datetime = start_walk_datetime + timedelta(minutes=40)
        # print(start_walk_datetime, end_walk_datetime)
        #
        # walk = Walk(user_id=1, started_at=start_walk_datetime, ended_at=end_walk_datetime)
        # session.add(walk)
        # session.commit()
        # session.close()

    for day in range(1, 13):
        for hour in range(8, 18):
            for miniute in range(0, 59):

                if random.randint(1, 3) % 2 == 0:
                    pull_datetime = datetime(2018, 5, day, hour, miniute, 0)

                    print(pull_datetime)
        #         if random.randint(1, 11) % 2:
        #             break
        #         pull_datetime = datetime(2018, 4, day, hour, miniute, 0)
        #
        #         print(pull_datetime)
        #
                    pull = Pull(user_id=1, created_at=pull_datetime)
                    session.add(pull)
                    session.commit()
                    session.close()
