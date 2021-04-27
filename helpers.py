from flask_login import login_user, logout_user
from  flask import session
import random

from mde.models import User
from mde import app, db


range_table_values =[2,3,4,5,6,7,8,9,10]

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
# { id:1, 'factor_a': 9, 'factor_b': 4, 'result': 36, 'user_result': None}
def get_multiplication_obj( range_from, range_to, id=1):
    range_from = int(range_from)
    range_to = int(range_to)

    factor_a = random.randint(range_from, range_to)
    factor_b = random.randint(range_from, range_to)
    return ({
            'id': id,
            'factor_a' : factor_a,
             'factor_b' : factor_b,
             'result' : factor_a * factor_b,
             'user_result' : None           
            })


# Function that receives a playform and save the play configuration into the session
def save_game_in_session(play_form):
    game = { 
        'range_from' : play_form.range_from.data,
        'range_to' : play_form.range_to.data,
        'amount' : play_form.amount.data,
        'mode' : play_form.mode.data,
        'exercises' : get_exercises(play_form.range_from.data, play_form.range_to.data, play_form.amount.data) 
    }
    session['game']= game

    # print('in save session: test ', session['game']['amount'])
    print(session['game'])



def remove_game_in_session():
    session.pop('game', None)
    