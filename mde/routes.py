from flask import render_template, flash, redirect, url_for, request
# I can also use the declarator loggin_required to force routes to be logged
from flask_login import login_user, logout_user, login_required, current_user

from mde import app, db
from mde.models import User
from mde.forms import RegisterForm

from helpers import userToCreate

@app.route('/')
@app.route('/home')
def home_page():
    # TODO: add logged declarator
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # app.logger.debug('test logger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()


    if request.method == 'POST' and form.validate_on_submit():   
        new_user = userToCreate(form)
        
        db.session.add(new_user)
        db.session.commit()

        # Log the created user. This will create a current_user, which will be available in every template
        login_user(new_user)
        
        flash( f"Account created successfully! You are now logged in as {new_user.username}.", category='success')
        return redirect(url_for('home_page'))
        

    # Display errors using flashing
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash( f'There was an error with creating a user: {err_msg}', category='danger' )


    # if request.method == 'GET':
    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    # built in fun in flask to logout users
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.errorhandler(404)
def page_not_found(error):
    # Note the 404 after the render_template() call. This tells Flask that the status code of 
    # that page should be 404 which means not found. By default 200 is assumed which 
    # translates to: all went well.
    return render_template('error.html', error=error), 404