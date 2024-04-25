import base64
import os

from flask import redirect, render_template, Blueprint, abort, request
from flask_login import login_required, current_user

from data.__all_models import *
from data.blueprints.main_bp import get_map1, get_map2, get_coordinates1, get_coordinates2
from server import db_session

blueprint = Blueprint('map_bp', __name__, template_folder='templates')


@blueprint.route('/add_map_kit', methods=['GET', 'POST'])
@login_required
def add_map_kit():
    from data.forms import MapHeadForm
    form = MapHeadForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = Maps1()
        maps.owner = current_user.id
        maps.city = form.city.data
        maps.name = form.name.data
        if not get_map1(get_coordinates1(maps.city), maps)[0]:
            render_template('error.html', error=get_map1(get_coordinates1(maps.city), maps)[1])
        db_sess.add(maps)
        db_sess.commit()
        return redirect('/')
    return render_template('mapadd.html', title='Добавление набора заметок', form=form)


@blueprint.route('/add_map/<name>', methods=['GET', 'POST'])
@login_required
def add_map(name):
    from data.forms import MapBodyForm1
    form = MapBodyForm1()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps1).filter(Maps1.owner == current_user.id, Maps1.name == name).first()
        mapp = Maps2()
        mapp.owner = current_user.id
        mapp.place = form.place.data
        mapp.text = form.text.data
        mapp.type = form.type.data
        if not get_map2(get_coordinates2(mapp.place), mapp)[0]:
            render_template('error.html', error=get_map2(get_coordinates2(mapp.place), mapp)[1])
        db_sess.add(mapp)
        db_sess.commit()
        maps.maps.append(mapp)
        db_sess.add(maps)
        db_sess.commit()
        return redirect('/')
    return render_template('mapadd.html', title='Добавление заметки в набор', form=form)


@blueprint.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    from data.forms import MapBodyForm2
    db_sess = db_session.create_session()
    MAPS = db_sess.query(Maps1).filter(Maps1.owner == current_user.id).all()
    form = MapBodyForm2()
    form.name.choices = [(i.name, i.name) for i in MAPS]
    form.name.choices.insert(0, ('-', '-'))
    maps = None
    if form.validate_on_submit():
        if form.name.data != '-':
            maps = db_sess.query(Maps1).filter(Maps1.owner == current_user.id, Maps1.name == form.name.data).first()
        mapp = Maps2()
        mapp.owner = current_user.id
        mapp.place = form.place.data
        mapp.text = form.text.data
        mapp.type = form.type.data
        if not get_map2(get_coordinates2(mapp.place), mapp)[0]:
            render_template('error.html', error=get_map2(get_coordinates2(mapp.place), mapp)[1])
        db_sess.add(mapp)
        db_sess.commit()
        if form.name.data != '-':
            maps.maps.append(mapp)
            db_sess.add(maps)
            db_sess.commit()
        return redirect('/')
    return render_template('mapadd.html', title='Добавление заметки', form=form)


@blueprint.route('/delete_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def delete_map(_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        maps = db_sess.query(Maps1).filter(Maps1.id == _id).first()
    else:
        maps = db_sess.query(Maps1).filter(Maps1.id == _id, Maps1.owner == current_user.id).first()
    if maps.maps:
        for map in maps.maps:
            db_sess.delete(map)
    db_sess.delete(maps)
    db_sess.commit()
    return redirect('/')


@blueprint.route('/delete_note/<int:_id>', methods=['GET', 'POST'])
@login_required
def delete_note(_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        note = db_sess.query(Maps2).filter(Maps2.id == _id).first()
    else:
        note = db_sess.query(Maps2).filter(Maps2.id == _id, Maps2.owner == current_user.id).first()
    if note.head:
        map = db_sess.query(Maps1).filter(Maps1.id == note.head).first()
        map.maps.remove(note)
    db_sess.delete(note)
    db_sess.commit()
    return redirect('/main/notes')


@blueprint.route('/choose_map/<int:_id>')
@login_required
def edit_maps(_id):
    db_sess = db_session.create_session()
    map = db_sess.query(Maps1).filter(Maps1.id == _id).first()
    return render_template('map_choose_change.html', title='Выбор заметки', maps=map.maps)


@blueprint.route('/change_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def change_maps(_id):
    from data.forms import MapBodyForm1
    form = MapBodyForm1()
    mapid = None
    if request.method == "GET":
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps2).filter(Maps2.id == _id).first()
        if maps:
            form.text.data = maps.text
            form.place.data = maps.place
            form.type.data = maps.type
            mapid = maps.id
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps2).filter(Maps2.id == _id).first()
        if maps:
            maps.text = form.text.data
            maps.place = form.place.data
            maps.type = form.type.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('mapadd.html', title='Редактирование заметки', form=form, mapid=mapid)


@blueprint.route('/add_image/<_id>', methods=['GET', 'POST'])
def upload_file(_id):
    from data.forms import UploadForm
    from server import photos
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps2).filter(Maps2.id == _id).first()
        with open(f'uploads/{filename}', 'rb') as img:
            image = Images()
            image.image = base64.b64encode(img.read()).decode('utf-8')
            maps.images.append(image)
        db_sess.add(maps)
        db_sess.commit()
        os.remove(f'uploads/{filename}')
        return redirect('/main/notes')
    return render_template('addim.html', form=form)

