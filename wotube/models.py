from flask_wtf import FlaskForm
from wotube import workout_db
from datetime import datetime
from flask_login import UserMixin
from wtforms import StringField, IntegerField, TextAreaField, URLField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, url, InputRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash


class Workout(workout_db.Model):
    id = workout_db.Column(workout_db.Integer, primary_key=True)
    title = workout_db.Column(workout_db.String(50), nullable=False)
    description = workout_db.Column(workout_db.String(300), nullable=False)
    category = workout_db.Column(workout_db.String(10), nullable=False)
    url = workout_db.Column(workout_db.Text, nullable=False)
    duration = workout_db.Column(workout_db.Integer, nullable=False)
    date = workout_db.Column(workout_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}>'


class User(UserMixin, workout_db.Model):
    id = workout_db.Column(workout_db.Integer, primary_key=True)
    username = workout_db.Column(workout_db.String(64), nullable=False, index=True, unique=True)
    email = workout_db.Column(workout_db.String(120), nullable=False, index=True, unique=True)
    password_hash = workout_db.Column(workout_db.String(128), nullable=False)
    joined_at_date = workout_db.Column(workout_db.DateTime(), index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}'"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class WorkoutForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    description = TextAreaField("description", validators=[InputRequired()])
    category = SelectField("Workout category:",
                           choices=[('full', 'Full Body'), ('upper', 'Upper Body'), ('lower', 'Lower Body'),
                                    ('core', 'Core')])
    url = URLField("url", validators=[DataRequired(), url()])
    duration = IntegerField("duration", validators=[InputRequired()])
    submit = SubmitField("Submit")
    update = SubmitField("Edit")
    remove = SubmitField("Remove")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
