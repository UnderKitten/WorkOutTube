from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, SubmitField, SelectField
from wtforms.validators import DataRequired, url, InputRequired
import creds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
workout_db = SQLAlchemy(app)
app.config['SECRET_KEY'] = creds.secret_key


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/library')
def library():
    workouts = Workout.query.all()
    return render_template("library.html", workouts=workouts)


@app.route('/library/<int:id>')
def workout_detail(id):
    workout = Workout.query.get(id)
    return render_template("workout-detail.html", workout=workout)


@app.route('/add_workout', methods=['POST', 'GET'])
def add_workout():
    new_workout = WorkoutForm()
    if request.method == "POST":
        workout = Workout(title=new_workout.title.data, description=new_workout.description.data
                          , category=new_workout.category.data, url=new_workout.url.data,
                          duration=new_workout.duration.data)
        try:
            workout_db.session.add(workout)
            workout_db.session.commit()
            return redirect('/library')
        except:
            return 'Something went wrong!'
    else:
        return render_template("add_workout.html", new_workout=new_workout)


@app.route('/library/<int:id>/edit', methods=['POST', 'GET'])
def edit_workout(id):
    workout = Workout.query.get(id)
    edited_workout = WorkoutForm(id=workout.id, title=workout.title, description=workout.description,
                                 category=workout.category,
                                 url=workout.url, duration=workout.duration, date=workout.date)
    if request.method == "POST":
        if edited_workout.update.data:
            workout.title = edited_workout.title.data
            workout.description = edited_workout.description.data
            workout.category = edited_workout.category.data
            workout.url = convert_url_to_embed(edited_workout.url.data)
            workout.duration = edited_workout.duration.data
            try:
                workout_db.session.commit()
                return redirect('/library')
            except:
                return 'Something went wrong!'
        elif edited_workout.remove.data:
            return redirect(f'/library/{id}/remove')
    else:
        return render_template("edit-workout.html", edited_workout=edited_workout)


@app.route('/library/<int:id>/remove')
def remove_workout(id):
    workout_to_remove = Workout.query.get(id)
    try:
        workout_db.session.delete(workout_to_remove)
        workout_db.session.commit()
        return redirect('/library')
    except:
        return "Something went wrong"


def convert_url_to_embed(url):
    url = url.replace("watch?v=", "embed/")
    return url


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


if __name__ == "__main__":
    app.run(debug=True)
