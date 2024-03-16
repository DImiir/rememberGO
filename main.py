from flask import Flask
from data import db_session
from data.__all_models import User
from data.blueprints import main_bp, map_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    app.register_blueprint(main_bp.blueprint)
    app.register_blueprint(map_bp.blueprint)
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/tables.sqlite")
    main()

