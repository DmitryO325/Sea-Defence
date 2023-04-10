import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Mail(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mails'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    attachments = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    user = orm.relationship("User")
