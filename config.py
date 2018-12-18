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
