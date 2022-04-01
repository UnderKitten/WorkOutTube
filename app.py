from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
workout_db = SQLAlchemy(app)


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
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        url = convert_url_to_embed(request.form['url'])
        duration = request.form['duration']

        workout = Workout(title=title, description=description, category=category, url=url, duration=duration)

        try:
            workout_db.session.add(workout)
            workout_db.session.commit()
            return redirect('/library')
        except:
            return 'Something went wrong!'
    else:
        return render_template("add_workout.html")


@app.route('/library/<int:id>/edit', methods=['POST', 'GET'])
def edit_workout(id):
    workout = Workout.query.get(id)
    if request.method == "POST":
        workout.title = request.form['title']
        workout.description = request.form['description']
        workout.category = request.form['category']
        workout.url = convert_url_to_embed(request.form['url'])
        workout.duration = request.form['duration']

        try:
            workout_db.session.commit()
            return redirect('/library')
        except:
            return 'Something went wrong!'
    else:
        return render_template("edit-workout.html", workout=workout)


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


if __name__ == "__main__":
    app.run(debug=True)
