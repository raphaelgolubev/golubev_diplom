# coding: utf8

from flask import Blueprint
from flask import render_template

devel = Blueprint('devel', __name__, template_folder='templates')
import sys
sys.path.append("c:\\Users\\User\\Documents\\golubev_diplom\\app")
from app import db

@devel.route('/dev')
def index():
    result1 = []
    for i in db.session.execute('show tables').fetchall():
        result1.append(str(i).replace('(','').replace(')','').replace("'","").replace(',',''))

    result2 = []
    columns = []
    for m in result1:
        for c in db.session.execute('show columns from ' + m).fetchall():
            columns.append({m:str(c[0]) + ": " + str(c[1])})

        for j in db.session.execute('select * from ' + m).fetchall():
            result2.append({m:j})

    return render_template('dev/index.html', cols = columns, tables=result1, result=result2)