from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    pwd = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Такой Email адрес уже существует')
        return redirect(url_for('auth.signup'))
    elif len(email) == 0:
        flash('Введите ваш email')
        return redirect(url_for('auth.signup'))
    elif len(name) == 0:
        flash('Введите ваше имя')
        return redirect(url_for('auth.signup'))
    elif len(pwd) == 0:
        flash('Введите ваш пароль')
        return redirect(url_for('auth.signup'))

    new_user = User()
    new_user.email=email
    new_user.name=name
    new_user.password=generate_password_hash(pwd, method='sha256')

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Пожалуйста, проверьте параметры Вашей учетной записи и попробуйте войти снова.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.search'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')
