from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_list.db'
workout_db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/library')
def library():
    return render_template("library.html")


@app.route('/add_workout', methods=['POST', 'GET'])
def add_workout():
    if request.method == "POST":
        pass
    else:
        return render_template("add_workout.html")


if __name__ == "__main__":
    app.run(debug=True)
