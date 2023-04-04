from dotenv import load_dotenv

import data.comment_resource
from data import db_session
from data.users import User
from flask import Flask, redirect, render_template
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.mail_form import MailForm
from flask_login import LoginManager, login_required, logout_user
from flask_login import login_user
from python.mail_sender import send_mail
from flask import send_from_directory, jsonify
from flask_restful import reqparse, abort, Api, Resource
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['Data'] = 'data'
api = Api(app)
api.add_resource(data.comment_resource.CommentsListResource, '/api/comments')
api.add_resource(data.comment_resource.CommentsResource, '/api/comments/<int:comment_id>')
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
            print('ok')
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
        user = User(name=form.name.data, email=form.email.data,
                    surname=form.surname.data, password=form.password.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/gallery')
def gallery():
    pass


@app.route('/reviews')
@login_required
def reviews():
    pass


@app.route('/download')
def download():
    return send_from_directory(app.config['Data'], 'game.zip', as_attachment=True)


@app.route('/mail', methods=['GET', 'POST'])
@login_required
def mail():
    form = MailForm()
    if form.validate_on_submit():
        print(form.topic.data, form.mail.data, form.attachments.data)
        send_mail('PS-4-2015@yandex.ru', form.topic.data, form.mail.data,
                  attachments=form.attachments.data)
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
