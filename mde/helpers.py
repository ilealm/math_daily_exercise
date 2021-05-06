from flask import flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask import session
import random
import time

from mde.models import User, Game
from mde import app, db


range_table_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Function that takes the new user information from a form and returns a User object.


def get_user_to_create(form):
    return User(
        username=form.username.data,
        email_address=form.email_address.data,
        password=form.password1.data,
        parent_email_address=form.parent_email_address.data)


# Function that calls User.add_new to inserts a new user into BD
def add_user(new_user):
    try:
        User.add_new(new_user)

    except AssertionError as error:
        app.logger.error(
            'An error occurred while adding the user into the database: ', error)


# Function that logs a user into the current session.
# This will create a current_user, which will be available in every template
def log_in_user(user):
    try:
        login_user(user)

    except AssertionError as error:
        app.logger.error(
            'An error occurred while login the user to the session: ', error)


def log_out_user():
    try:
        logout_user()

    except AssertionError as error:
        app.logger.error('An error occurred while logout the user: ', error)


# function that check if a username exists in the database
def get_user(username_to_check):
    try:
        return User.get_user_by_username(username_to_check)

    except AssertionError as error:
        app.logger.error(
            'An error occurred while validating if the username exists: ', error)


# function that check if an attempted password is the same as the User.password_hash
def is_user_password(user, password_to_check):
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


# Function that receives a game configuration and set the session['game'] with it
def save_game_in_session(play_form):
    game_mode = play_form.mode.data
    base_game = {
        'range_from': play_form.range_from.data,
        'range_to': play_form.range_to.data,
        'mode': game_mode,
        'amount': play_form.amount.data, 
        'right_answers': None,
        'assertiveness': None,
        'start_timestap': time.time(),
        'timespan': None,
    }

    #  I can create a base game, and use spread operator to unify the objects and create the game object
    if game_mode == "Exercises":
        config_game = {
            'time_played' : None,
            'exercises': get_exercises(play_form.range_from.data, play_form.range_to.data, play_form.amount.data)
        }
    
    if game_mode == "Minutes":
        config_game = {
            # TODO update this amount on save game to DB with the right amount of solved questions
            'time_played' : int(play_form.amount.data),
            'exercises': get_exercises(play_form.range_from.data, play_form.range_to.data, int(play_form.range_exersices.data))
        }

    game = { **base_game, **config_game }


    session['game'] = game
    session.permanent = False



# Boolean function that receives the user's answers and validate if at least one has value
def at_least_one_answer(user_answers):
    for op in user_answers:
        if not op['user_answer'] == None:
            return True 
    
    return False

# Function that receives the user's answers, and with it update the session game and register the game into DB.
def process_game(user_answers):    
    update_game_in_session_answers(user_answers)
    save_game_in_db()
    update_user_stats(session['game']['right_answers'])
 


# Function that receives an array with a copy of session[game][operations] but with user answers.
# The user answers will be added to the sesssion, and [game][right_answers] will be updated, in a string format.
# Also, the amount of right answers will be counted and updated to [session][game][right_answers]
def update_game_in_session_answers(user_answers):  
    end_timestap =  time.time()
    right_answers = 0
    answered_exercises = 0  # to keep a control of the real amount of answered questions

    session['game']['exercises'] = user_answers

    for op in session['game']['exercises']:
        if not op['user_answer'] == None:
            answered_exercises += 1 
            op['user_answer'] = str(op['user_answer'])
            if op['user_answer'] == op['result']:
                right_answers += 1

    
    # I'm only updatig session[game] if the user has answered something
    if answered_exercises > 0:
        session['game']['amount'] = answered_exercises
        session['game']['right_answers'] = right_answers
        session['game']['assertiveness'] = round( 
            ((right_answers / answered_exercises) * 100), 2)    
        session['game']['timespan'] = get_timestamp(session['game']['start_timestap'], end_timestap)
        # BC the session won't automatically detect changes to mutable data types (list, dictionary, set, etc.)
        # I need to tell it that has been updated
        session.modified = True
    

def get_timestamp(start_timestap, end_timestap):
    game_time = end_timestap - session['game']['start_timestap']
    game_minutes = round(game_time // 60)
    game_seconds = round(game_time % 60)

    game_minutes =  ("00" + str(game_minutes))[-2:]
    game_seconds =  ("0" + str(game_seconds))[-2:]

    game_timespan = game_minutes + ":" + game_seconds
    return game_timespan


def save_game_in_db():
    try:
        current_game = session['game']
        game = Game(
            range_from=current_game['range_from'],
            range_to=current_game['range_to'],
            amount=current_game['amount'],
            mode=current_game['mode'],
            right_answers=current_game['right_answers'],
            assertiveness=current_game['assertiveness'],
            timespan=current_game['timespan'],
            user_id=current_user.id
        )
        Game.add_new(game)   

    except AssertionError as error:
        app.logger.error(
            'An error occurred while adding the game into the database: ', error)


# function that update user's stats with the last game played
def update_user_stats(num_right_answers):
    try:
        current_user.update_stats(num_right_answers)

    except AssertionError as error:
        app.logger.error(
            'An error occurred while updating the usert game stats into the database: ', error)



# Function that returns true/false if the object session['game'] exists
def session_game_exits():
    if not 'game' in session:
        return False
    return True


def remove_game_in_session():
    session.pop('game', None)


