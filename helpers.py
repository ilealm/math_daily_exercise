from flask_login import login_user, logout_user
from flask import session
import random

from mde.models import User
from mde import app, db


range_table_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Function that takes the new user information from a form, and returns it a User object.


def getUserToCreate(form):
    return User(
        username=form.username.data,
        email_address=form.email_address.data,
        password=form.password1.data,
        parent_email_address=form.parent_email_address.data)


# Helper function that inserts a new user into BD
def addUser(new_user):
    try:
        db.session.add(new_user)
        db.session.commit()
    except AssertionError as error:
        app.logger.error(
            'An error occurred while adding the user into the database: ', error)


# Function that logs a user into the current session.
# This will create a current_user, which will be available in every template
def logInUser(user):
    try:
        login_user(user)
    except AssertionError as error:
        app.logger.error(
            'An error occurred while login the user to the session: ', error)


def logOutUser():
    try:
        logout_user()
    except AssertionError as error:
        app.logger.error('An error occurred while logout the user: ', error)


# function that check if a username exists in the database
def getUser(username_to_check):
    try:
        return User.query.filter_by(username=username_to_check).first()
    except AssertionError as error:
        app.logger.error(
            'An error occurred while validating if the username exists: ', error)


# function that check if an attempted password is the same as the User.password_hash
def isUserPassword(user, password_to_check):
    try:
        return user.check_password_correction(attempted_password=password_to_check)
    except AssertionError as error:
        app.logger.error(
            'An error occurred while validating if the attempted password is correct: ', error)


# Function thar returns an array with N multiplication objects for a given tables range.
# If N (amount) is not especified, then only 1 exercise is returned
def get_exercises(range_from, range_to, amount=1):
    exercises = []
    for i in range(amount):
        exercises.append(get_multiplication_obj(range_from, range_to, i))

    return exercises


# Function that given range, returns a single object with factor a, factor b, the multiplication result and user result with value none
# { num_operacion:1, 'factor_a': 9, 'factor_b': 4, 'result': 36, 'user_answer': None}
def get_multiplication_obj(range_from, range_to, id=1):
    range_from = int(range_from)
    range_to = int(range_to)

    factor_a = random.randint(range_from, range_to)
    factor_b = random.randint(range_from, range_to)
    return ({
            'num_operacion': id,
            'factor_a': factor_a,
            'factor_b': factor_b,
            'result': factor_a * factor_b,
            'user_answer': None
            })


# Function that receives a playform and save the play configuration into the session
def save_game_in_session(play_form):
    game = {
        'range_from': play_form.range_from.data,
        'range_to': play_form.range_to.data,
        'amount': play_form.amount.data,
        'mode': play_form.mode.data,
        'exercises': get_exercises(play_form.range_from.data, play_form.range_to.data, play_form.amount.data),
        'right_answers': None
    }
    session['game'] = game
    session.permanent = False




# Function that receives an array with a copy of session[game][operations] but with user answers.
# The user answers will be added to the sesssion, and [game][right_answers] will be updated, in a string format.
# Also, the amount of right answers will be counted and updated to [session][game][right_answers] 
def update_game_in_session_answers(user_answers):
    # TODO: validate that the session object exists
    if not 'game' in session:
        return

    session['game']['exercises'] = user_answers

    right_answers = 0
    for op in session['game']['exercises']:
        op['user_answer'] = str(op['user_answer'])
        if op['user_answer'] == op['result']:
            right_answers += 1
    
    session['game']['right_answers'] = right_answers

 
    # BC the session won't automatically detect changes to mutable data types (list, dictionary, set, etc.)
    # I need to tell it that has been updated
    session.modified = True


    # print('\n\n\n in update_game_in_session_answers\n', session['game'], '\n')
    






def remove_game_in_session():
    session.pop('game', None)

