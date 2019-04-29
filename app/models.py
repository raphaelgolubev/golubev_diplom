# coding: utf8
from app import db, login
import sys, inspect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

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
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 1:1 Profile <-> User
    profile = db.relationship('Profile', backref='user_profile', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id:{}, username:{} >'.format(self.id, self.username)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    language = db.Column(db.String(255))
    scope = db.Column(db.String(255))
    about = db.Column(db.String(255))
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    lastseen = db.Column(db.DateTime, default=datetime.utcnow)
    activity = db.Column(db.Boolean)
    projects = db.Column(db.String(255))
    algorithms = db.Column(db.String(255))
    templates = db.Column(db.String(255))
    # 1:1 Profile <-> User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    # *args - список неявно указанных аргументов
    # **kwargs - Key Words Args - именованные аргументы
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Profile user_id:{}, user_name:{}, lastseen: {} >'.format(self.user_id, self.user_name, self.lastseen)
