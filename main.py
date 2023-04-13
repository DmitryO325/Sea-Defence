import datetime
import os

import flask
from dotenv import load_dotenv
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from data.mails import Mail
from data.reviews import Review
import data.review_resource
from data import db_session
from data.users import User
from flask import Flask, redirect, render_template, request
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.mail_form import MailForm
from data.review_form import ReviewForm
from flask_login import LoginManager, login_required, logout_user
from flask_login import login_user, current_user
from python.mail_sender import send_mail
from flask import send_from_directory, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['Data'] = 'data'
app.config['UPLOAD_FOLDER'] = 'uploads'
api = Api(app)
api.add_resource(data.review_resource.ReviewsListResource, '/api/reviews')
api.add_resource(data.review_resource.ReviewsResource, '/api/reviews/<int:review_id>')
load_dotenv()
db_session.global_init("db/data_base.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # Функция для получения пользователя
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.surname = form.surname.data
        user.password = form.password.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/reviews')
@login_required
def reviews():
    return render_template('reviews.html')


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    form = ReviewForm()

    if form.validate_on_submit():
        attachments = []

        review = Review()
        review.user_id = current_user.id
        review.topic = form.topic.data
        review.review = form.review.data
        review.attachments = ', '.join(attachments)
        review.send_date = datetime.datetime.now()

        session = db_session.create_session()
        session.add(review)
        session.commit()

        return redirect('/reviews')

    return render_template('write_review.html', form=form)


@app.route('/download')
def download():
    return send_from_directory(app.config['Data'], 'game.zip', as_attachment=True)


@app.route('/mail', methods=['GET', 'POST'])
@login_required
def mail():
    form = MailForm()

    if form.validate_on_submit():
        attachments = []
        files = request.files.getlist(form.attachments.name)

        for file in files:
            file_name = secure_filename(file.filename)
            attachments.append(file_name)
            file.save(f'{app.config["UPLOAD_FOLDER"]}/{file_name}')

        send_mail('PS-4-2015@yandex.ru', form.topic.data, form.mail.data,
                  attachments=attachments)

        email = Mail()
        email.topic = form.topic.data
        email.attachments = ', '.join(attachments)
        email.user_id = current_user.id
        email.content = form.mail.data

        session = db_session.create_session()
        session.add(email)
        session.commit()
        return redirect('/')

    return render_template('mail.html', form=form)


@app.errorhandler(401)
def error_401(error):
    return redirect('/login')


@app.errorhandler(500)
@app.errorhandler(404)
def error_handler(error):
    if error.code == 500:
        return render_template('error.html', message='Возникла непредвиденная ошибка, '
                                                     'но она в скором времени будет устранена. '
                                                     'Пожалуйста, перейдите на главную страницу')
    if error.code == 404:
        return render_template('error.html', message='К сожалению, данного материала не существует, '
                                                     'но, возможно, ее добавят в будущем. '
                                                     'Пожалуйста, перейдите на главную страницу')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
