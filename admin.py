from flask import Response, redirect
from flask_admin.contrib import sqla
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from model import db, User


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            message, 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class ModelView(sqla.ModelView):

    column_display_pk = True

    def is_accessible(self):
        from app import admin_basic_auth

        if not admin_basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        from app import admin_basic_auth

        return redirect(admin_basic_auth.challenge())


class RoleView(ModelView):
    form_choices = {
        'name': [
            ('admin', 'admin'),
            ('general', 'general')
        ]
    }


def init_admin(app_obj):
    admin = Admin(app_obj, name='Spajam2018_SP', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session, category='User'))
