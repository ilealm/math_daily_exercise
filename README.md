

# Dependencies

Database:
pip install flask-sqlalchemy

To hash passwords:
pip install flask_bcrypt

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'

# Start Server

python run.py

#