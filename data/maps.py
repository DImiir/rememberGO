import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Maps(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'maps'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    type = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    text = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    places = sqlalchemy.Column(sqlalchemy.String)
    map = sqlalchemy.Column(sqlalchemy.String)
