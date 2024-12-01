
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

@bp.cli.command("init_data")
def init_data():  # Preset data for testing and initial deployment 
  """Add initial dbug data to db"""

  User.query.delete()
  Task.query.delete()

  user = User(username="demo",
           email="demo@demo.com",
           display_name="Demo User",           
           access=40)
  user.set_password("train")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)    

  task = Task(name = "Todo List App",
           description = "Write ToDo list app for Software Assessment Task",
           category = "School")  
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)    

  task = Task(name = "Clean Bedroom",
           description = "Find what smells and get rid of it!",
           category = "Home")  
  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)    

  task = Task(name = "Maths Assignment",
           description = "Study for Maths",
           category = "School")

  user.tasks.append(task)
  db.session.commit() 
  print("Created:", task)    
  
  

  user = User(username="fred",
           email="fred@fullsteam.net",
           display_name="Fred",                      
           access=10)
  user.set_password("fred")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)  
  
  
