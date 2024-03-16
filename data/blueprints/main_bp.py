import requests
from flask import redirect, render_template, Blueprint
from flask_login import login_user, current_user, login_required, logout_user
from data.__all_models import LoginForm, RegisterForm, User
from data import db_session
from werkzeug.security import generate_password_hash

from data.maps import Maps

blueprint = Blueprint('main_bp', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/main')
def main():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps).filter(Maps.owner == current_user.id)
        return render_template('real_main.html', maps=maps)
    return render_template('base.html')


@blueprint.route('/main/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@blueprint.route('/main/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', form=form, current_user=current_user)


@blueprint.route('/main/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

