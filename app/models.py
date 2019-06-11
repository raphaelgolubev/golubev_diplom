# coding: utf8
from app import db, login
from app import app
from time import time
import jwt
import sys, inspect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

STANDART_PHOTO = '../static/root/assets/user.png'

#возвращает классы данного модуля
def get_classes():
    return inspect.getmembers(sys.modules[__name__], inspect.isclass)
#получить объект класса по названию
def get_class(name):
    for i in get_classes():
        if i[0].lower() == name.lower():
            return i[1]
        else:
            return 'none'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_login = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirmed = db.Column(db.String(10), default='False')
    password_hash = db.Column(db.String(128))
    # 1:1 Profile <-> User
    profile = db.relationship('Profile', backref='user_profile', uselist=False)
    role = db.Column(db.String(120), default='User')

    def get_email_confirm_token(self, expires_in=200):
        return jwt.encode(
            {'confirm_link_token': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY_EMAIL_CONFIRM'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_confirm_email_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY_EMAIL_CONFIRM'], algorithms=['HS256'])['confirm_link_token']
        except:
            return
        return User.query.get(id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id:{}, user_login:{} >'.format(self.id, self.user_login)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column(db.String(32))
    photo = db.Column(db.String(255), default=STANDART_PHOTO)
    lastseen = db.Column(db.DateTime, default=datetime.utcnow)
    # 1:1 Profile <-> User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    # 1:1 Profile <-> BaseSettings
    base_settings = db.relationship('BaseSettings', backref='profile_baseSettings', uselist=False)
    templates = db.relationship('CodeTemplate', backref='profile_templates')

    # *args - список неявно указанных аргументов
    # **kwargs - Key Words Args - именованные аргументы
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Profile id:{}, lastseen:{} >'.format(self.id, self.lastseen)
class BaseSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), index=True, unique=True)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    projects = db.Column(db.String(255))
    programming_langs = db.Column(db.String(255))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), unique=True)

    # *args - список неявно указанных аргументов
    # **kwargs - Key Words Args - именованные аргументы
    def __init__(self, *args, **kwargs):
        super(BaseSettings, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<BaseSettings id:{}>'.format(self.id)

class CodeTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    lang = db.Column(db.String(140))
    short_name = db.Column(db.String(64))
    code = db.Column(db.Text)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __init__(self, *args, **kwargs):
        super(CodeTemplate, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<CodeTemplate id:{}, name:{}>'.format(self.id, self.name)

