from app import app, db
import os
from email_work import send_password_reset_email
from forms import LoginForm, MainSettingsForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from models import User, Profile
from flask_login import current_user, login_user, logout_user,login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #создаем юзера
        user = User(username=form.username.data, email=form.email.data)
        #задаем пароль с помощью функции хэширования
        user.set_password(form.password.data)
        #создаем профиль
        user_profile = Profile(username=form.username.data)
        #связываем модели
        user.profile = user_profile
        db.session.add(user)
        db.session.add(user_profile)

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
            user = User.query.filter_by(username=form.username.data).first()
            #проверка пароля
            if user is None or not user.check_password(form.password.data):
                flash('Неверное имя пользователя или пароль.')
                return redirect(url_for('login'))
                
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
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
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('main'))

@app.route('/user/<username>')
@login_required
def user(username):
    form = MainSettingsForm()
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user, form=form)

from config import Configuration
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS

from werkzeug.utils import secure_filename
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
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
            return redirect(url_for('user', username=current_user.username))

    