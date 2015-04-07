import os

SECRET_KEY = 'random_secret_key_here'

basedir = os.path.abspath(os.path.dirname(__file__))

# for sqlite:
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
JSON_AS_ASCII = False

# email server sender details
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "user@gmail.com"
MAIL_PASSWORD = "pass"

ADMINS = ['adminmail@gmail.com']
HOST_ROOT = 'http://www.google.com'

MEDIA_ROOT = os.path.join(basedir, 'app/static/media')
MEDIA_URL  = 'app/static/media'
STATIC_ROOT = os.path.join(basedir, 'app/static/css')
STATIC_URL =  'app/static/css'
