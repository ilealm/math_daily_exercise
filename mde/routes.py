from flask import render_template, flash, redirect, url_for, request

from mde import app, db
from mde.models import User
from mde.forms import RegisterForm


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

    if form.validate_on_submit():
        user_to_create = User(
                            username = form.username.data,
                            email_address = form.email_address.data,
                            password = form.password1.data,
                            parent_email_address = form.parent_email_address.data     )
        db.session.add(user_to_create)
        db.session.commit()
        # print('user added')
        flash( f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
        
        
        # TODO: hash password: done
        # TODO: log the new user to the session
        # TODO: have parent psw optional
        # TODO: clear form
        # TODO: add login_required to routes
        # TODO: fix closing error window
        # TODO: align register form components

    # Display errors using flashing
    if form.errors != {}:
        # print('there were errors....')
        for err_msg in form.errors.values():
            flash( f'There was an error with creating a user: {err_msg}', category='danger' )
        
    return render_template('register.html', form=form)




@app.errorhandler(404)
def page_not_found(error):
    # Note the 404 after the render_template() call. This tells Flask that the status code of 
    # that page should be 404 which means not found. By default 200 is assumed which 
    # translates to: all went well.
    return render_template('error.html', error=error), 404