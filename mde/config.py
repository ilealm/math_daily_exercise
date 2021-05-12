from os import environ, path
# I need to install python-dotenv to use this file
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))



# base config
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'
DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///mde.db'



