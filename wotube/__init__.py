from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wotube import creds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
workout_db = SQLAlchemy(app)
app.config['SECRET_KEY'] = creds.secret_key

from wotube import routes
