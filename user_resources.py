from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.__all_models import User
from reqparse import parser


class UsersResource(Resource):
    def get(self, user_id):
        self.abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'news': users.to_dict(
            only=('surname', 'name', 'email'))})

    def delete(self, user_id):
        self.abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_users_not_found(self, user_id):
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        if not users:
            abort(404, message=f"User {user_id} not found")


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User()
        users.surname = args['surname'],
        users.name = args['name'],
        users.age = args['age'],
        users.position = args['position'],
        users.speciality = args['speciality'],
        users.address = args['address'],
        users.email = args['email'],
        users.modified_date = args['modified_date']
        users.password(args['hashed_password'])
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})
