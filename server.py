from flask import Flask
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

from data import db_session
from data.__all_models import User
from data.blueprints import main_bp, map_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

app.register_blueprint(main_bp.blueprint)
app.register_blueprint(map_bp.blueprint)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/tables.sqlite")
    app.run()


if __name__ == '__main__':
    main()
