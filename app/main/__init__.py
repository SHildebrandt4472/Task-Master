
from flask import Blueprint, render_template #, request 
from flask_login import current_user
from app.models.user import login
from app.utils import helpers


def error_forbidden(e):
  return render_template('403.html'), 403


bp = Blueprint('main', __name__)

def init_app(app):
    app.register_blueprint(bp)
    app.register_error_handler(403, error_forbidden)
    app.jinja_options['finalize'] = lambda x: x if x is not None else '' #prevent Jinja from printing None

    login.login_view = 'main.login'
    login.init_app(app)

    @app.context_processor
    def inject_default_template_variables():   
         return dict(h=helpers)
    
    

    @app.before_request
    def update_last_seen():
      if current_user.is_authenticated:
        current_user.update_last_seen()

from . import main_routes







