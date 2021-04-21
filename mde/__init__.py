from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'
app.config['SECRET_KEY'] = 'b59f86b27719b42ba5a635e4' 
db = SQLAlchemy(app)

# Login/register mgnt
bcrypt = Bcrypt(app)


from mde import routes