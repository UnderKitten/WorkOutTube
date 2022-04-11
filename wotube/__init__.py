from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from wotube import creds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
workout_db = SQLAlchemy(app)
app.config['SECRET_KEY'] = creds.secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from wotube import routes
