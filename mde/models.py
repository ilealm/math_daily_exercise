from datetime import datetime
from mde import bcrypt


from mde import db



class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    parent_email_address = db.Column(db.String(length=50), nullable=True)
    games_played = db.Column(db.Integer(), nullable=True, default=0)
    last_played = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

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