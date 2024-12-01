import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): #This is the main configurations for the app
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'todo.db') 
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = "ThisIsMySuperSecretKey"  