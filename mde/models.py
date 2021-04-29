from datetime import datetime
from mde import bcrypt
# for login mgnt
# UserMixin: this class inherits is_authenticated, is_active, is_annonymous, get_id. 
# So I don't have to implemented as it says in the docs.
# I must add it in the User class
from flask_login import UserMixin

from mde import db, login_manager


# flask_login manager. This is the one that will be accesible from all pages
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# for login mgnt
# UserMixin: this class inherits is_authenticated, is_active, is_annonymous, get_id. 
# So I don't have to implemented as it says in the docs.
# I must add it in the User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    parent_email_address = db.Column(db.String(length=50), nullable=True, default=None)
    games_played = db.Column(db.Integer, nullable=True, default=0)
    last_played = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    # BC user can have n games, I can create a relationship 1:n
    # backref is a simple way to also declare a new property on the Game class. 
    # You can then also use my_game.user to get to the user at that game.
    # In this case we told it to point to the Game class and load multiple of those
    # Lazy = true: SQLAlchemy will load the data as necessary in one go using a standard select statement
    # A query object equivalent to a dynamic user.addresses relationship can be created using Address.query.with_parent(user) 
    games = db.relationship('Game', backref='user', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.username

    # this property is called routes.py/register_page(), on_submit, while creating a new user
    @property
    def password(self):
        return self.password

    
    # this method will be called by @property
    @password.setter
    def password(self, plain_text_password):    
        # overwrite what is going to be store in password_hash
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    

    # to check if the psw is valid while login 
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    

    def increase_game(self):
        self. games_played += 1
        # self.last_played = datetime.utcnow
        db.session.commit()

    
    

class Game(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    
    range_from = db.Column(db.Integer, nullable=False)
    range_to = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(length=10), nullable=False)
    right_answers = db.Column(db.Integer, nullable=False)
    assertiveness = db.Column(db.Float, nullable=False)
    # relationship to the user. 'user.id' must be in lower case
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Game %r>' % self.id