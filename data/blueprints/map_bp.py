from flask import redirect, render_template, Blueprint, abort, request
from flask_login import login_required, current_user
from data.__all_models import Maps1, MapForm, Maps2
from data import db_session


blueprint = Blueprint('map_bp', __name__, template_folder='templates')


@blueprint.route('/add_map', methods=['GET', 'POST'])
@login_required
def add_map():
    form = MapForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        maps = db_sess.query(Maps1).filter(Maps1.owner == current_user.id, Maps1.city == form.city.data).first()
        if maps:
            mapp = Maps2()
            mapp.owner = maps.owner
            mapp.place = form.place.data
            mapp.text = form.text.data
            db_sess.add(mapp)
            db_sess.commit()
            maps.maps += f', {mapp.id}'
        else:
            maps = Maps1()
            maps.owner = current_user.id
            maps.city = form.city.data
            mapp = Maps2()
            mapp.owner = maps.owner
            mapp.place = form.place.data
            mapp.text = form.text.data
            db_sess.add(mapp)
            db_sess.commit()
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


@blueprint.route('/add_map/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_maps(_id):
    form = MapForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            maps = db_sess.query(Maps1).filter(Maps1.id == _id).first()
        else:
            maps = db_sess.query(Maps1).filter(Maps1.id == _id, Maps1.owner == current_user.id).first()
        if maps:
            form.city.data = maps.city
            texts = []
            for num in maps.maps.split(', '):
                map = db_sess.query(Maps2).filter(Maps2.id == int(num)).first()
                texts.append(map.text)
            form.text.data = '\n'.join(texts)
            form.place.data = map.places
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            maps = db_sess.query(Maps1).filter(Maps1.id == _id).first()
        else:
            maps = db_sess.query(Maps1).filter(Maps1.id == _id, Maps1.owner == current_user.id).first()
        if maps:
            maps.text = form.text.data
            maps.places = form.place.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('mapadd.html', title='Редактирование заметки', form=form)

