import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Captcha(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'captchas'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_email = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.email"), nullable=False)
    code = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    is_activated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    email = orm.relationship("User")