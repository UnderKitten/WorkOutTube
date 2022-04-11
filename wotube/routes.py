import email_validator

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from wotube import app, workout_db, login_manager
from wotube.models import Workout, WorkoutForm, RegistrationForm, User, LoginForm


@app.route('/')
def index():
    # clear_data()
    return render_template("index.html")


@app.route('/library')
@login_required
def library():
    # log_user = User.query.filter_by(username=username).first_or_404()
    # workouts = Workout.query.filter_by(user_id=log_user.id)
    # if workouts is None:
    #     workouts = []
    workouts = Workout.query.all()
    return render_template("library.html", workouts=workouts)


@app.route('/library/<int:id>')
def workout_detail(id):
    workout = Workout.query.get(id)
    return render_template("workout-detail.html", workout=workout)


@app.route('/add_workout', methods=['POST', 'GET'])
@login_required
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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("register")
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        workout_db.session.add(new_user)
        workout_db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = LoginForm(request.form)
    # if request.method == "POST":
    if form.validate_on_submit():
        print("validate")
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index', _external=True))
        else:
            flash('Login Unsuccessful. Please check email and login', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index', _external=True))


def convert_url_to_embed(url):
    url = url.replace("watch?v=", "embed/")
    return url


def clear_data():
    workout_db.drop_all()
    workout_db.create_all()
    workout_db.session.commit()
