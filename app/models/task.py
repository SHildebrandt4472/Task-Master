#from flask import current_app as app, session, g
from app.models import db
import datetime

STS_NEW = 0
STS_COMPLETED = 1

P_LOW = 0
P_MEDIUM = 1
P_HIGH = 2

PRIORITY_STRS = ['Low', 'Medium','High']

# Define the Task model
class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
  name = db.Column(db.String(32))                      
  description = db.Column(db.String(250))                 
  category = db.Column(db.String(10))   
  priority = db.Column(db.Integer,default=P_LOW)              
  status = db.Column(db.Integer,default=STS_NEW) 
  due_by = db.Column(db.DateTime)         
  created_at = db.Column(db.DateTime, default=db.func.datetime('now'))

#Define all little functions to check the status of the task
  def __repr__(self):
    return f"<Task {self.id}: {self.name}>"   

  def done(self):
    self.status = STS_COMPLETED 

  def undo(self):
    self.status = STS_NEW    

  def is_outstanding(self):
    return self.status < STS_COMPLETED

  def is_completed(self):
    return self.status == STS_COMPLETED

  def is_important(self):
    if self.priority and self.priority > P_LOW:
      return True

  def is_overdue(self):
    if self.is_completed():
      return False
    else:
      return self.due_by and self.due_by.date() < datetime.date.today() 

  def is_coming_up(self):
    if self.is_completed():
      return False
    else:
      next_week = datetime.date.today() + datetime.timedelta(days=7)
      return self.due_by and self.due_by.date() < next_week
  
  def is_recently_added(self):
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    return self.created_at and self.created_at.date() > last_week

  def priority_str(self):    
    priority = self.priority or 0
    if priority >= 0 and priority < len(PRIORITY_STRS):
      return PRIORITY_STRS[priority]
    return ''

  def status_str(self):
    if self.status == STS_COMPLETED:
      return 'Completed'
    return 'Outstanding'
  
  def short_desc(self):
    desc = self.description
    if len(desc) > 40:
      desc = desc[:37] + " ..." 
    return desc  