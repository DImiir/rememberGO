import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Maps1(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mapsH'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    city = sqlalchemy.Column(sqlalchemy.String)
    maps = sqlalchemy.Column(sqlalchemy.String)

