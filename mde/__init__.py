from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'
# app.config['SECRET_KEY'] = '9375c6484ab92cb1271e95f5' # this will config later
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    parent_email_address = db.Column(db.String(length=50), nullable=True, unique=True)
    

from mde import routes