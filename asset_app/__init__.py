
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()

app.config['SECRET_KEY'] = 'JUSgPqv4hN'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message='Для доступа пожалуйста авторизуйтесь!'
login_manager.login_message_category='success'



import asset_app.modul.views
from asset_app.auth.views import auth
app.register_blueprint(auth)
login_manager.init_app(app)