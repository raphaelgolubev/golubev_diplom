from app import app, db
from forms import LoginForm, RegistrationForm
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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #проверка юзера
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #проверка пароля
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile.html', user=user, posts=posts)
    