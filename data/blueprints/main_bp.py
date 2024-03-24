import requests
from flask import redirect, render_template, Blueprint
from flask_login import login_user, current_user, login_required, logout_user
from data.__all_models import LoginForm, RegisterForm, User
from data import db_session

from data.maps_head import Maps1
from data.maps_body import Maps2

blueprint = Blueprint('main_bp', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/main')
def main():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps1).filter(Maps1.owner == current_user.id)
        responses = []
        for _ in maps:
            texts, places = [], []
            for map in _.maps.split(', '):
                mapp = db_sess.query(Maps2).filter(Maps2.id == int(map)).first()
                texts.append(mapp.text)
                places.append(mapp.place)
            responses.append(get_map(get_coordinates1(_.city), places, _.city))
        return render_template('real_main.html', responses=responses, texts=texts)
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
        login_user(user)
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
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'features' in data:
            if data['features']:
                coordinates = data['features'][0]['geometry']['coordinates']
                return f'{coordinates[::-1][1]},{coordinates[::-1][0]}'
            else:
                return None
        else:
            print("Ошибка при получении данных:", data)
            return None
    except Exception as e:
        print("Произошла ошибка при выполнении запроса:", e)
        return None


def get_map(ll, places, city):
    map_params = {"ll": ",".join([str(ll[0]), str(ll[1])]), 'l': 'map',
                  "pt": "~".join([get_coordinates2(f'{city},{point}') + f',pmwtm{num + 1}'
                                  for num, point in enumerate(places)])}
    map_api_server = "http://static-maps.yandex.ru/1.x/?apikey=fbd7d1f6-f3ac-4002-91a2-cc0552631701&size=300,300&l=map&"
    response = f'{map_api_server}ll={map_params["ll"]}&pt={map_params["pt"]}'
    return response


