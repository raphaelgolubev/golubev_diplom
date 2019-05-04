import os, urllib

class Configuration(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'raphael-golubev-is1-15-super-secret-key'

    #надстройки для sql
    # СТРОКА ПОДКЛЮЧЕНИЯ:
    # MYSQL: mysql+mysqlconnector://username:password@localhost/databasename
    # Ноутбук в фта: mysql+mysqlconnector://raphael:12345@localhost/MyTestRaphaelDB
    # Microsoft SQL Server (pymssql): mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8
    # Microsoft SQL Server (pyodbc): 
    # import urllib
    # params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=servername;DATABASE=master;Trusted_Connection=yes;')
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=РАФАЭЛЬ-ПК;DATABASE=master;Trusted_Connection=yes;')
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #куда будут складываться файлы, которые юзер отправит на сервер
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SESSION_TYPE = 'filesystem'