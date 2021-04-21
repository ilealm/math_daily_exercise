from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'
# app.config['SECRET_KEY'] = '9375c6484ab92cb1271e95f5' # this will config later
db = SQLAlchemy(app)

from mde import routes