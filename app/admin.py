import os.path as op

from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView


from app import app, db
from app.models import User

admin = Admin(app, name='Admin', template_mode='bootstrap3')

class ModelView(ModelView):
    def is_accessible(self):
        auth = request.authorisation or request.environ.get('REMOTE_USER')
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('You have to be an administrator.', 401,
                                             {'WWW-Authenticate': 'Basic realm="login Required"'}
                                             ))
        return True
    #users
    admin.add_view(ModelView(User, db.session))

    #static files
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static'))
