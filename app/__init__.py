from flask import Flask
app = Flask(__name__)

#setup the application with the config.py file
app.config .from_object('app.config')

#setup the logger
from app.logger_setup import logger

#setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

#setup the mail server
from flask_mail import Mail
mail = Mail(app)

#setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

#setup the password crypting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#import the views
from app.views import user
app.register_blueprint(user.userbp)

#setup the login process
from flask_login import LoginManager
from app.models import User, Accounts, Stock

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'

@login_manager.user_loader
def load_user(first_name):
    return User.query.filter(User.first_name == first_name).first()


from app import admin






