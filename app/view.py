from app import app, db
import os
from email_work import send_password_reset_email
from forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from models import User, Profile, BaseSettings, CodeTemplate
from flask_login import current_user, login_user, logout_user,login_required
from flask import render_template, flash, redirect, url_for, request, abort
from werkzeug.urls import url_parse
from functools import wraps
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.profile.active = 'Онлайн'
        current_user.profile.lastseen = datetime.utcnow()
        db.session.commit()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role != 'admin':
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('forbidden.html')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/library')
def library():
    templs = CodeTemplate.query.all()
    return render_template('library.html', templates=templs)

@app.route('/library/<id>')
def template_page(id):
    id = int(id)
    templs = CodeTemplate.query.all()
    for templ in templs:
        if templ.id == id:
            return render_template('template_page.html', templ=templ)
    abort(404)

@app.route('/my_templates')
@login_required
def my_templates():
    return render_template('my-templates.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #создаем юзера
        user = User(user_login=form.user_login.data, email=form.email.data)
        #задаем пароль с помощью функции хэширования
        user.set_password(form.password.data)
        #создаем профиль для подачи в них основных данных
        user_profile = Profile()
        #теперь создаем БАЗОВЫЕ настройки создаваемого юзера
        profile_base = BaseSettings(username=form.username.data)
        
        #связываем модели
        #BaseSettings --ЗАСУНУЛИ В--> Profile
        user_profile.base_settings = profile_base
        #Profile --ЗАСУНУЛИ В--> User
        user.profile = user_profile
        #Всё это скомпановано в объект user, добавляем его в сессию
        db.session.add(user)
        #Сохраняем изменения
        db.session.commit()
        flash('Вы успешно зарегистрировались.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #проверка юзера
    if current_user.is_authenticated:
        flash('Авторизация прошла успешно.')
        return redirect(url_for('main'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(user_login=form.user_login.data).first()
            #проверка пароля
            if user is None or not user.check_password(form.password.data):
                flash('Неверное имя пользователя или пароль.')
                return redirect(url_for('login'))
                
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main')

            return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Проверьте адрес электронной почты на корректность для отправки пароля.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль был изменён.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/logout')
def logout():   
    if current_user.is_authenticated: 
        current_user.profile.active = 'Не в сети'
        db.session.commit()
        logout_user()
        return redirect(url_for('main'))
    return 'hi'

@app.route('/user/<username>')
@login_required
def user(username):
    users = User.query.all()
    for user in users:
        if (user.profile.base_settings.username):
            if (user.profile.base_settings.username == username):
                return render_template('profile.html', user=user)
    abort(404)

from config import Configuration
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS

from werkzeug.utils import secure_filename
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'avatar' not in request.files:
            flash('No file part: {}'.format(request.files))
            return redirect(request.url)
        file = request.files['avatar']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and user:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile.photo = '..' + os.path.join(app.config['FOLDER_POSTFIX'], filename)
            db.session.commit();
            return redirect(url_for('user', username=current_user.profile.base_settings.username))

    