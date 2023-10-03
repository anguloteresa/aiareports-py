import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class Config(object):
  SECRET_KEY = os.getenv("SECRET_KEY")
  DEBUG = False
  TESTING = False
  SESSION_TYPE = 'sqlalchemy'
  UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=" + os.getenv('PROD_ODBC')
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

class TestingConfig(Config):
  DEBUG = True
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
