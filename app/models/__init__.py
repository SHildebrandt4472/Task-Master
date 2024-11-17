

from .base import db, migrate
from .user import User
from .task import Task

def init_app(app):
    db.init_app(app);
    migrate.init_app(app,db)





