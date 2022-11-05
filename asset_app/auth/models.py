from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo

from asset_app import db, app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pwdhash = db.Column(db.String(500), nullable=False)

    def __init__(self, username, psw):
        self.username = username
        self.pwdhash = generate_password_hash(psw)

    def __repr__(self):
        return f'{self.username},  {self.pwdhash}'




class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired(), EqualTo('confirm', message='Пароли должны совподать')])
    confirm = PasswordField('Повторите пароль', validators=[InputRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired()])
    password = PasswordField('Введите пароль', validators=[InputRequired()])
    remainme = BooleanField('Запомнить', default=False)
    submit = SubmitField('Отправить')




def register_user(user):
    pass


def login_user(user, password):
   pass