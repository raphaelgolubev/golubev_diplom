#coding:utf-8
from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

#точко входа flask-приложения
app = Flask(__name__)
app.config.from_object(Configuration)

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
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'root.oneproject@gmail.com',
	MAIL_PASSWORD = 'gieivoksolvwctry'
	)
#почта
from flask_mail import Mail
mail = Mail(app)

#регистрация блюпринтов
from dev.blueprint import devel
app.register_blueprint(devel, prefix_url='/dev')

# последним шагом импортируется вьюха
import view

@app.shell_context_processor
def make_shell_context():
    return {'db': db}