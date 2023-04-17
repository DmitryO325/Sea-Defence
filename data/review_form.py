from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    topic = StringField(validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Опубликовать отзыв')
