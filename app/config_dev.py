import logging
import os

from app.config_common import*
FLASKY_COMMENTS_PER_PAGE = 20

#DEBUG can only be set True in a development environment for security reasons
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

#secret key for generating tokens
SECRET_KEY = 'okothogodo'

#Admin credentials
ADMIN_CREDENTIALS =('admin', 'pa$$word')

#Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///guchashop.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True


#configuration of a gmail account for sending emails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['mikeogodo5@gmail.com']

#number of times password is hashed
BCRYPT_LOG_ROUNDS = 12
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'ApplicationActivity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2
