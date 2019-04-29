from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Configuration)

##Тут я протестировал GIT
##и еще раз

#Реализация авторизации
from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import User, Profile

db.create_all()
db.session.commit()

from dev.blueprint import devel
#регистрация блюпринтов
app.register_blueprint(devel, prefix_url='/dev')

import view