
#
#  Command Line Interface
#
#  These functions can be accessed from command line as follows....
#
#    flask cli COMMAND [ARGS]
#
#  A list of avaiable commands can be generated with ...
#
#    flask cli
#
#
import click
from app.models import db, User, Task
from app.cli import bp
import datetime

@bp.cli.command("init_data")
def init_data():  # Preset data for testing and initial deployment 
  """Add initial dbug data to db"""

  User.query.delete()
  Task.query.delete()
  
  user = User(username="sam",  # Creating a new user with differents attributes
              email="sam@fullsteam.net",
              display_name="Sam")              
  user.set_password("train")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)  

  user = User(username="demo",  # Creating a new demo user with differents attributes
           email="demo@demo.com",
           display_name="Demo User")             
  user.set_password("demo")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)    

  task = Task(name = "Todo List App",
           description = "Write ToDo list app for Software Assessment Task",
           category = "School",
           status = 1,
           due_by = datetime.date(2024, 12, 4))  
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)    

  task = Task(name = "Clean Bedroom",
           description = "Find what smells and get rid of it!",
           category = "Home",
           due_by = datetime.date.today() - datetime.timedelta(days=100))    
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)    

  task = Task(name = "Maths Assignment",
           description = "Study for Maths",
           category = "School",
           priority = 2,
           due_by = datetime.date(2024, 12, 2))
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      

  task = Task(name = "Demo 1",
           description = "An Important task",
           category = "Demo",
           priority = 2,           
           due_by = datetime.date.today())
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      

  task = Task(name = "Demo 2",
           description = "An medium Priority Task",
           category = "Demo",                 
           due_by = datetime.date.today() + datetime.timedelta(days=5))
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      

  task = Task(name = "Demo 3",
           description = "An important Task way in the future",
           category = "Demo",
           priority = 1,           
           due_by = datetime.date.today() + datetime.timedelta(days=60))
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      

  task = Task(name = "Demo 4",
           description = "A completed Task",
           category = "Demo",           
           status = 1,
           due_by = datetime.date.today() - datetime.timedelta(days=1))
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      

  task = Task(name = "Demo 5",
           description = "A recently added task",
           category = "Demo",                      
           due_by = datetime.date.today() + datetime.timedelta(days=20))
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)      




  
  
  
