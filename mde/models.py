from datetime import datetime

from mde import db



class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    parent_email_address = db.Column(db.String(length=50), nullable=True)
    games_played = db.Column(db.Integer(), nullable=True, default=0)
    last_played = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)