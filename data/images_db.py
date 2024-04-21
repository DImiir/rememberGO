import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Images(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_map = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mapsB.id"))
    image = sqlalchemy.Column(sqlalchemy.String, default=None)

