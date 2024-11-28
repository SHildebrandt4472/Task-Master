#from flask import current_app as app, session, g
from app.models import db

STS_NEW = 0
STS_COMPLETED = 1

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
  name = db.Column(db.String(32))                      
  description = db.Column(db.String(250))                 
  category = db.Column(db.String(10))                 
  status = db.Column(db.Integer) 
  due_by = db.Column(db.DateTime)         
  created_at = db.Column(db.DateTime, default=db.func.datetime('now'))      

  def __repr__(self):
    return f"<Task {self.id}: {self.name}>"   

  def done(self):
    self.status = STS_COMPLETED 




