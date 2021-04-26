from flask_login import login_user, logout_user  # , login_required, current_user


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
