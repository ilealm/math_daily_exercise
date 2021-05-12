from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# # with this, I import the config file
app.config.from_pyfile('config.py')




db = SQLAlchemy(app)

# Login/register mgnt
bcrypt = Bcrypt(app)

# Login Management
login_manager = LoginManager(app)
# especify where the login route is located, so I can use login declarators in my routes, and redirect the user when needed.
login_manager.login_view = "login_page" # expects the login route
login_manager.login_message = "Please login to access this page."
# this is for display flash messages
login_manager.login_message_category = 'info'


from mde import routes