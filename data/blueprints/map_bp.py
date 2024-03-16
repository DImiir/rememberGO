import requests
from flask import redirect, render_template, Blueprint, abort, request
from flask_login import login_required, current_user
from data.__all_models import Maps, MapForm
from data import db_session


blueprint = Blueprint('map_bp', __name__, template_folder='templates')


@blueprint.route('/add_map', methods=['GET', 'POST'])
@login_required
def add_map():
    form = MapForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps).filter(Maps.owner == current_user.id, Maps.city == form.city.data).first()
        if maps:
            maps.type = form.type.data
            maps.text += f';;;{form.text.data}'
            maps.places += f';;;{form.place.data}'
            maps.map = f'{get_map(get_coordinates(form.city.data), 10, maps.places)}'
        else:
            maps = Maps()
            maps.owner = current_user.id
            maps.type = form.type.data
            maps.text = form.text.data
            maps.city = form.city.data
            maps.places = form.place.data
            maps.map = f'{get_map(get_coordinates(form.city.data), 10, maps.places)}'
        db_sess.add(maps)
        db_sess.commit()
        return redirect('/')
    return render_template('mapadd.html', title='Добавление заметки', form=form)


@blueprint.route('/delete_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def delete_map(_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        maps = db_sess.query(Maps).filter(Maps.id == _id).first()
    else:
        maps = db_sess.query(Maps).filter(Maps.id == _id, Maps.owner == current_user.id).first()
    if maps:
        db_sess.delete(maps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@blueprint.route('/add_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_maps(_id):
    form = MapForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            maps = db_sess.query(Maps).filter(Maps.id == _id).first()
        else:
            maps = db_sess.query(Maps).filter(Maps.id == _id, Maps.owner == current_user.id).first()
        if maps:
            form.type.data = maps.type
            form.text.data = maps.text
            form.city.data = maps.city
            form.place.data = maps.places
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            maps = db_sess.query(Maps).filter(Maps.id == _id).first()
        else:
            maps = db_sess.query(Maps).filter(Maps.id == _id, Maps.owner == current_user.id).first()
        if maps:
            maps.type = form.type.data
            maps.text = form.text.data
            maps.places = form.place.data
            maps.map = f'{get_map(get_coordinates(form.city.data), 10, maps.places)}'
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('mapadd.html', title='Редактирование заметки', form=form)


def get_coordinates(address):
    url = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
           f'geocode={address}&format=json')
    data = requests.get(url).json()
    geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    coordinates = map(float, geo_object['Point']['pos'].split(' '))
    return list(coordinates)


def get_map(ll, z, places):
    map_params = {"ll": ",".join([str(ll[0]), str(ll[1])]), "z": z, 'l': 'map'}
    map_api_server = "http://static-maps.yandex.ru/1.x/?apikey=fbd7d1f6-f3ac-4002-91a2-cc0552631701&size=300,300&"
    response = f'{map_api_server}ll={map_params["ll"]}&z={map_params["z"]}&l=map'
    return response

