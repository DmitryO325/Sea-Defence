import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.INTEGER, sqlalchemy.ForeignKey("users.id"), nullable=False)
    topic = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    review = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    send_date = sqlalchemy.Column(sqlalchemy.DATETIME, default=datetime.datetime.now())
    user = orm.relationship("User")
