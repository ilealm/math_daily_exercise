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