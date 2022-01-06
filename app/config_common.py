TIMEZONE = 'Europe/Paris'


#secret key for generating tokens
SECRET_KEY = 'okothogodo'

#admin credentials
ADMIN_CREDENTIALS = ('admin','pa$$word')

#Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///guchashop.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True


#configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
ADMINS = ''


#Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12
