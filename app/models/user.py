
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from datetime import datetime

login = LoginManager()

ACCESS = {
  'none'     :  0,
  'basic'    : 10,
  'advanced' : 20,
  'admin'    : 30,
  'super'    : 40, 
}

ACCESS_STRS = {
  ACCESS['none']    : "No Access",
  ACCESS['basic']   : "Standard",
  ACCESS['advanced']: "Advanced",
  ACCESS['admin']   : "Admin",
  ACCESS['super']   : "Super",
}

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(32), index=True, unique=True)
  display_name = db.Column(db.String(32))
  school_id = db.Column(db.Integer)
  access = db.Column(db.Integer, default=ACCESS['basic'])

  email = db.Column(db.String(120), index=True, unique=True)
  email_verified = db.Column(db.Integer)
  password_hash = db.Column(db.String(128))
  last_seen = db.Column(db.DateTime) 
  created_at = db.Column(db.DateTime, default=db.func.datetime('now')) #default=db.func.utc_timestamp())
  last_modified = db.Column(db.DateTime, default=db.func.datetime('now'), onupdate=db.func.datetime('now')) #, default=db.func.utc_timestamp(), onupdate=db.func.utc_timestamp())

  tasks = db.relationship('Task', backref='user', lazy=True)

  def __repr__(self):
    return f"<User {self.id}: {self.username}>"

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    if not self.password_hash:
      return False
    return check_password_hash(self.password_hash, password)

  def is_basic(self):
    return self.access >= ACCESS['basic']

  def is_advanced(self):
    return self.access >= ACCESS['advanced']

  def is_admin(self):
    return self.access >= ACCESS['admin']

  def is_super(self):
    return self.access >= ACCESS['super']

  def set_admin(self):
    self.access = ACCESS['admin']
  
  def name(self):
    return self.display_name or self.username

  def access_str(self):
    if self.access in ACCESS_STRS:
      return ACCESS_STRS[self.access]
    return "Unknown"

  def update_last_seen(self):
    last_seen = self.last_seen if self.last_seen else datetime.fromtimestamp(0)
    if (datetime.utcnow() - last_seen).total_seconds() > 600:  # More than 10 minutes ago
     #print(f"Update Last Seen: {last_seen}")
     self.last_seen = datetime.utcnow()
     db.session.commit()

@login.user_loader
def load_user(id):
  return User.query.get(int(id))


