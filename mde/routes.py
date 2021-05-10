from flask import render_template, flash, redirect, url_for, request, session
# I can also use the declarator loggin_required to force routes to be logged
# from flask_login import login_user, logout_user, login_required, current_user
from flask_login import login_required, current_user

from mde import app  # , db
from mde.models import User
from mde.forms import RegisterForm, LoginForm, PlayForm, GameForm, GameByTimeForm
from wtforms.validators import ValidationError

# user management
from mde.helpers import get_user_to_create, add_user, log_in_user, log_out_user, get_user, is_user_password
# session management
from mde.helpers import save_game_in_session, remove_game_in_session, session_game_exits
# game management
from mde.helpers import range_table_values, process_game, at_least_one_answer


@app.route('/')
@app.route('/home')
def home_page():
    # process_game([])
    return render_template('home.html')


@app.route('/play', methods=['GET', 'POST'])
@login_required
def play_page():
    form = PlayForm()

    if form.validate_on_submit():
        # clean if I have a past game
        remove_game_in_session()
        save_game_in_session(form)
        return redirect(url_for('game_page'))

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There were errors while creating the game: {err_msg}', category='danger')

    # if I got here, I need to clean the past game, if there is one
    remove_game_in_session()
    return render_template('play.html', form=form, range_table_values=range_table_values)


# Route that handles the user's game in  "Exersices" mode, meaning the user want to try a fixed amount of excersices.
@app.route('/game', methods=['GET', 'POST'])
@login_required
def game_page():
    if not 'game' in session:
        flash(f'Please configure your game to start playing. ', category='danger')
        return redirect(url_for('play_page'))

    # get the number of exersices to perform. If is in "Exercise" mode will the the amount, otherwhise will be the value of the trying combo
    user_operations = session['game']['exercises']
    # because I know how many operations I need to display, I need to pass the operations as argument . form = GameForm() will only put 1 empty row
    form = GameForm(operations=user_operations)

    if form.validate_on_submit():
        # I'm going to get all the user answers into an array
        user_answers = []
        for field in form.operations:
            user_answers.append(field.data)

        if not at_least_one_answer(user_answers):
            flash(f'You didn\'t answer any exercise.', category='danger')
            return redirect(url_for('play_page'))


        process_game(user_answers)
        return redirect(url_for('results_page'))

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There were errors while checking the game: {err_msg}', category='danger')

    return render_template('game.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results_page():
    # session['game'] is set on play/POST. A game must be configure to enter this route
    if not 'game' in session:
        flash(f'Please configure your game to start playing. ', category='danger')
        return redirect(url_for('play_page'))

    return render_template('results.html')


@app.route('/stats')
@login_required
def stats_page():
    return render_template('stats.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = get_user(form.username.data)
        if attempted_user:
            if is_user_password(attempted_user, form.password.data):
                flash(
                    f'Success! You are logged in as: {attempted_user.username}', category='success')
                log_in_user(attempted_user)
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
        new_user = get_user_to_create(form)
        add_user(new_user)
        log_in_user(new_user)

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
    log_out_user()
    remove_game_in_session()

    flash("You have been logged out!", category='info')

    return redirect(url_for("home_page"))


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(error):
    # Note the 404 after the render_template() call. This tells Flask that the status code of
    # that page should be 404 which means not found. By default 200 is assumed which
    # translates to: all went well.
    return render_template('error.html', error=error), 404



