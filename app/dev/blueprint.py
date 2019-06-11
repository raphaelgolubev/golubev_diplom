# coding: utf8

from flask import Blueprint
from flask import render_template
from view import admin_required
from flask_login import login_required

devel = Blueprint('devel', __name__, template_folder='templates')
import sys
sys.path.append("c:\\Users\\User\\Documents\\golubev_diplom\\app")
from app import db
from models import User

@devel.route('/dev')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('dev/index.html', users=users)