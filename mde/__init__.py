from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'
app.config['SECRET_KEY'] = 'b59f86b27719b42ba5a635e4' 
db = SQLAlchemy(app)

from mde import routes