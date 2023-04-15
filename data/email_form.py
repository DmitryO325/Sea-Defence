from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class EmailForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    submit = SubmitField('Восстановить пароль')