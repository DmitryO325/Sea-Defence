import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    registration_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())

    def set_password(self, password1):
        self.password = generate_password_hash(password1)

    def check_password(self, password1):
        return check_password_hash(self.password, password1)
