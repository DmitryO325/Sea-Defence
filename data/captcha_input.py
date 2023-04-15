from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired


class CaptchaForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    captcha = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Подтвердить ввод')