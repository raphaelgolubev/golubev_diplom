#coding:utf-8
from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

#точко входа flask-приложения
app = Flask(__name__)
app.config.from_object(Configuration)
#модуль для решения проблем со временем
moment = Moment(app)

#Реализация авторизации
from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

# ИНИЦИАЛИЗАЦИЯ БД И МИГРАЦИИ
db = SQLAlchemy(app)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#обновляем только конфиги почты
app.config.update(
	#EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TSL = False,
	MAIL_USE_SSL = True,
    MAIL_USERNAME = '4acm.adm@gmail.com',
    MAIL_PASSWORD = 'rravjcyxojqqtecm'
	)
#почта
from flask_mail import Mail
mail = Mail(app)

#регистрация блюпринтов
from dev.blueprint import devel
app.register_blueprint(devel, prefix_url='/dev')


import view # последним шагом импортируется вьюха
import ajax # и вьюха обрабатывающая запросы на сервер

@app.shell_context_processor
def make_shell_context():
    return {'db': db}