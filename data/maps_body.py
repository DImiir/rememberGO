import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Maps2(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mapsB'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mapsH.owner"))
    place = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Boolean)

