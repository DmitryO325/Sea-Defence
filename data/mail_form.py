from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


class MailForm(FlaskForm):
    topic = StringField(validators=[DataRequired()])
    mail = TextAreaField(validators=[DataRequired()])
    attachments = MultipleFileField()
    submit = SubmitField('Отправить письмо')