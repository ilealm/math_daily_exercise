from flask import render_template, flash, redirect, url_for, request, session
# I can also use the declarator loggin_required to force routes to be logged
# from flask_login import login_user, logout_user, login_required, current_user
from flask_login import login_required, current_user

from mde import app  # , db
from mde.models import User
from mde.forms import RegisterForm, LoginForm, PlayForm, GameForm
from wtforms.validators import ValidationError

# user management
from helpers import getUserToCreate, addUser, logInUser, logOutUser, getUser, isUserPassword
# session management
from helpers import save_game_in_session, remove_game_in_session
from helpers import range_table_values


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/play', methods=['GET', 'POST'])
@login_required
def play_page():
    form = PlayForm()

    if form.validate_on_submit():
        remove_game_in_session()
        save_game_in_session(form)
        # range_from = form.range_from.data
        # range_to = form.range_to.data
        # amount =  form.amount.data
        # mode = form.mode.data
        # exercises = get_exercises(range_from, range_to, amount) 
        # session permanent = False #  If set to False (which is the default) the session will be deleted when the user closes the browser.

        # if form.mode.data == 'Exercises':            
        return redirect(url_for('game_page'))
            

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There were errors while creating the game: {err_msg}', category='danger')

    return render_template('play.html', form=form, range_table_values=range_table_values)




@app.route('/game', methods=['GET', 'POST'])
@login_required
def game_page():
    # session['game'] is set on play/POST. A game must be configure to enter this route
    if not 'game' in session:
        flash(f'Please configure your game to start playing. ', category='danger')
        return redirect(url_for('play_page'))

    user_operations = session['game']['exercises']
    # because I know how many operations I need to display, I need to pass the operations as argument . form = GameForm() will only put 1 empty row 
    form = GameForm(operations=user_operations)
    
    # TODO: validate integer input
    if form.validate_on_submit():
        for field in form.operations:
            print(field.data)
        
        # for value in form.operations.data:
        #     print(value)

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There were errors while checking the game: {err_msg}', category='danger')

   
    return render_template('game.html', form=form)



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
