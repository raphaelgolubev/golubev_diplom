import os

class Configuration(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'raphael-golubev-is1-15-super-secret-key'

    #надстройки для sql
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://raphael:12345@localhost/MyTestRaphaelDB"
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #куда будут складываться файлы, которые юзер отправит на сервер
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SESSION_TYPE = 'filesystem'