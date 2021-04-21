from flask import render_template

from mde import app
from mde.models import User


@app.route('/')
@app.route('/home')
def home_page():
    # TODO: add logged declarator
    return render_template('home.html')



@app.route('/login')
def login_page():
    return render_template('login.html')




@app.errorhandler(404)
def page_not_found(error):
    # Note the 404 after the render_template() call. This tells Flask that the status code of 
    # that page should be 404 which means not found. By default 200 is assumed which 
    # translates to: all went well.
    return render_template('error.html', error=error), 404