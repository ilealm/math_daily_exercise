from os import environ, path
# I need to install python-dotenv to use this file
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# DB config
SQLALCHEMY_DATABASE_URI = 'sqlite:///mde.db'
SECRET_KEY = environ.get('SECRET_KEY')