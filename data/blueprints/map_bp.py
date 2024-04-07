from flask import redirect, render_template, Blueprint, abort, request
from flask_login import login_required, current_user
from data.__all_models import *
from data import db_session


blueprint = Blueprint('map_bp', __name__, template_folder='templates')


@blueprint.route('/add_map_kit', methods=['GET', 'POST'])
@login_required
def add_map_kit():
    form = MapHeadForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = Maps1()
        maps.owner = current_user.id
        maps.city = form.city.data
        maps.name = form.name.data
        db_sess.add(maps)
        db_sess.commit()
        return redirect('/')
    return render_template('mapadd.html', title='Добавление набора заметок', form=form)


@blueprint.route('/add_map/<name>', methods=['GET', 'POST'])
@login_required
def add_map(name):
    form = MapBodyForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps1).filter(Maps1.owner == current_user.id, Maps1.name == name).first()
        mapp = Maps2()
        mapp.owner = maps.owner
        mapp.place = form.place.data
        mapp.text = form.text.data
        mapp.type = form.type.data
        db_sess.add(mapp)
        db_sess.commit()
        if maps.maps:
            maps.maps += f', {mapp.id}'
        else:
            maps.maps = f'{mapp.id}'
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
    if maps:
        for num in maps.maps.split(', '):
            map = db_sess.query(Maps2).filter(Maps2.id == num).first()
            db_sess.delete(map)
        db_sess.delete(maps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@blueprint.route('/choose_map/<int:_id>')
@login_required
def edit_maps(_id):
    db_sess = db_session.create_session()
    map = db_sess.query(Maps1).filter(Maps1.id == _id).first()
    maps = map.maps.split(', ')
    return render_template('map_choose_change.html', title='Выбор заметки', maps=maps)


@blueprint.route('/change_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def change_maps(_id):
    form = MapForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps2).filter(Maps2.id == _id).first()
        if maps:
            form.text.data = maps.text
            form.place.data = maps.place
            form.type.data = maps.type
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
    return render_template('mapadd.html', title='Редактирование заметки', form=form)
