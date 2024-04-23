from flask import redirect, render_template, Blueprint
from flask_login import login_user, current_user, login_required, logout_user
from data.__all_models import *
from data import db_session
import requests

blueprint = Blueprint('main_bp', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/main')
@blueprint.route('/main/kits')
def main_kits():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        MAPS = db_sess.query(Maps1).filter(Maps1.owner == current_user.id).all()
        if current_user.id == 1:
            MAPS = db_sess.query(Maps1).filter().all()
        data = []
        for map in MAPS:
            data.append((get_map1(get_coordinates1(map.city), map), map))
        return render_template('main_kits.html', data=data)
    return render_template('base.html')


@blueprint.route('/main/notes')
def main_notes():
    db_sess = db_session.create_session()
    MAPS = db_sess.query(Maps1).filter(Maps1.owner == current_user.id)
    if current_user.id == 1:
        MAPS = db_sess.query(Maps1).filter().all()
    data = []
    for map in MAPS:
        for note in map.maps:
            data.append((get_map2(get_coordinates2(note.place), note, map.city), note))
    return render_template('main_notes.html', data=data)


@blueprint.route('/main/register', methods=['GET', 'POST'])
def reqister():
    from data.forms import RegisterForm
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
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@blueprint.route('/main/login', methods=['GET', 'POST'])
def login():
    from data.forms import LoginForm
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


def get_coordinates1(address):
    url = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
           f'geocode={address}&format=json')
    data = requests.get(url).json()
    geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    coordinates = map(str, geo_object['Point']['pos'].split(' '))
    return list(coordinates)


def get_coordinates2(place_name):
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    url = f'https://search-maps.yandex.ru/v1/?text={place_name}&type=biz&lang=ru_RU&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'features' in data:
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return f'{coordinates[::-1][1]},{coordinates[::-1][0]}'
        else:
            return None


def get_map1(ll, maps):
    points = []
    for num in range(len(maps.maps)):
        points.append(f"{get_coordinates2(f'{maps.city},{maps.maps[num].place}')},pmwtm{num + 1}")
        if maps.maps[num].type:
            points.append(f"{get_coordinates2(f'{maps.city},{maps.maps[num].place}')},pmgrm{num + 1}")
    map_params = {"ll": ",".join([str(ll[0]), str(ll[1])]), 'l': 'map', "pt": '~'.join(points)}
    map_api_server = "http://static-maps.yandex.ru/1.x/?apikey=fbd7d1f6-f3ac-4002-91a2-cc0552631701&size=300,300&l=map&"
    return f'{map_api_server}ll={map_params["ll"]}&pt={map_params["pt"]}'


def get_map2(ll, map, city):
    point = f"{get_coordinates2(f'{city},{map.place}')},pmwtm"
    if map.type:
        point = f"{get_coordinates2(f'{city},{map.place}')},pmgrm"
    map_params = {"ll": ll, 'l': 'map', "pt": point, "z": 13}
    map_api_server = "http://static-maps.yandex.ru/1.x/?apikey=fbd7d1f6-f3ac-4002-91a2-cc0552631701&size=300,300&l=map&"
    return f'{map_api_server}ll={map_params["ll"]}&pt={map_params["pt"]}&z={map_params["z"]}'
