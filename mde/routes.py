from flask import render_template, flash, redirect, url_for, request
# I can also use the declarator loggin_required to force routes to be logged
# from flask_login import login_user, logout_user, login_required, current_user
from flask_login import login_required, current_user

from mde import app  # , db
from mde.models import User
from mde.forms import RegisterForm, LoginForm, PlayForm
from wtforms.validators import ValidationError

from helpers import getUserToCreate, addUser, logInUser, logOutUser, getUser, isUserPassword
from helpers import range_table_values, get_exercises

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/play', methods=['GET', 'POST'])
@login_required
def play_page():
    form = PlayForm()

    if form.validate_on_submit():
        range_from = form.range_from.data
        range_to = form.range_to.data
        amount =  form.amount.data
        mode = form.mode.data
   
        if mode == 'Exercises':            
            return render_template('game.html', exercises=get_exercises(range_from, range_to, amount) )

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There were errors while creating the game: {err_msg}', category='danger')

    return render_template('play.html', form=form, range_table_values=range_table_values)



@app.route('/game')
@login_required
def game_page():
    return home_template('home.html')



@app.route('/stats')
@login_required
def stats_page():
    return render_template('error.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = getUser(form.username.data)
        if attempted_user:
            if isUserPassword(attempted_user, form.password.data):
                flash(
                    f'Success! You are logged in as: {attempted_user.username}', category='success')
                logInUser(attempted_user)
                return redirect(url_for('home_page'))
            else:
                flash('Invalid password! Please try again', category='danger')
        else:
            flash('Invalid user name! Please try again', category='danger')

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_user = getUserToCreate(form)
        addUser(new_user)
        logInUser(new_user)

        flash(
            f"Account created successfully! You are now logged in as {new_user.username}.", category='success')
        return redirect(url_for('home_page'))

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logOutUser()

    flash("You have been logged out!", category='info')

    return redirect(url_for("home_page"))


@app.errorhandler(404)
def page_not_found(error):
    # Note the 404 after the render_template() call. This tells Flask that the status code of
    # that page should be 404 which means not found. By default 200 is assumed which
    # translates to: all went well.
    return render_template('error.html', error=error), 404
