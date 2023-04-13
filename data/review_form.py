from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    topic = StringField(validators=[DataRequired()])
    review = TextAreaField(validators=[DataRequired()])
    attachments = MultipleFileField()
    submit = SubmitField('Опубликовать отзыв')
