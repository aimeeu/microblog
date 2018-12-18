from application import db, login_manager
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(Config.USER_ABOUT_ME_MAX_LENGTH))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # The backref argument defines the name of a field that will be
    # added to the Post class that points back at the User
    # object. This will add a
    # post.author expression that will return the user given a post.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, UserID {}, Email {}>'.format(self.username, self.id, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''
        Gravatar is a Globally Recognized Avatar.
        You upload it and create your profile just once,
        and then when you participate in any Gravatar-enabled site,
        your Gravatar image will automatically follow you there.
        By default, images are presented at 80px by 80px if no size parameter
        is supplied
        :param size:  1 up to 2048 (px)
        :return: Gravatar image url for an image src tag
        '''
        my_email = self.email.strip()
        my_email_lower = my_email.lower()
        digest = md5(my_email_lower.encode('utf8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}; Author {}; Avatar URL {}>'.format(self.body, self.author.username, self.author.avatar(36))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'body': self.body,
            'userId': self.user_id
        }


@login_manager.user_loader
def load_user(user_id):
    """
    Required by Flask-Login to be implemented
    :param user_id:
    :return: User
    """
    return User.query.get(int(user_id))
