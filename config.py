import os

basedir = os.path.abspath(os.path.dirname(__file__))

'''
The SECRET_KEY configuration variable that I added as the only 
configuration item is an important part in most Flask applications. 
Flask and some of its extensions 
use the value of the
secret key as a cryptographic key, useful to generate signatures or tokens. 
The Flask-WTF ex-
tension uses it to protect web forms against a nasty attack called 
Cross-Site Request Forgery 6
or CSRF (pronounced “seasurf”).
'''


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'superSecretKey'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'microblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_ABOUT_ME_MAX_LENGTH = 140
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['aimeeu.opensource@gmail.com']
    POSTS_PER_PAGE = 50
