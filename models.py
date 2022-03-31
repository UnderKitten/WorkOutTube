from app import workout_db
from datetime import datetime


class Workout(workout_db.Model):
    id = workout_db.Column(workout_db.Integer, primary_key=True)
    title = workout_db.Column(workout_db.String(50), nullable=False)
    description = workout_db.Column(workout_db.String(300), nullable=False)
    category = workout_db.Column(workout_db.String(10), nullable=False)
    url = workout_db.Column(workout_db.Text, nullable=False)
    date = workout_db.Column(workout_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}>'
