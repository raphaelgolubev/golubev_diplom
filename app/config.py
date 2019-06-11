import os, urllib

class Configuration(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'raphael-golubev-is1-15-super-secret-key'
    SECRET_KEY_EMAIL_CONFIRM = 'secret-key-for-confirm-email-link'
    #надстройки для sql
    # СТРОКА ПОДКЛЮЧЕНИЯ:
    # MYSQL: mysql+mysqlconnector://username:password@localhost/databasename
    # Ноутбук в фта: mysql+mysqlconnector://raphael:12345@localhost/MyTestRaphaelDB
    # Microsoft SQL Server (pymssql): mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8
    # Microsoft SQL Server (pyodbc): 
    # import urllib
    # params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=servername;DATABASE=master;Trusted_Connection=yes;')
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123@localhost/flaskTest"
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #куда будут складываться файлы, которые юзер отправит на сервер
    FOLDER_POSTFIX = '\\static\\root\\assets\\uploads'
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + FOLDER_POSTFIX
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SESSION_TYPE = 'filesystem'

    ADMINS = ['4acm.adm@gmail.com']