from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = '206f66b5a40dc04517831de15f682596' # will be protecting us from attacks and ensure safe cookies
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"


db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

from flaskblog import routes


