from flask_login import login_user #, logout_user, login_required, current_user


from mde.models import User
from mde import app, db


# Function that takes the new user information from a form, and returns a User object.
def userToCreate(form):
    return User(
                username = form.username.data,
                email_address = form.email_address.data,
                password = form.password1.data,
                parent_email_address = form.parent_email_address.data  )



# Helper function that inserts a new user into BD
def addUser(new_user):
    try:
        db.session.add(new_user)
        db.session.commit()
    except AssertionError as error:
        app.logger.error('An error occurred while adding the user into the database: ', error)



# Function that logs a user into the current session.
# This will create a current_user, which will be available in every template
def logUser(user):
    try:
        login_user(user)
    except AssertionError as error:
        app.logger.error('An error occurred while login the user to the session: ', error)