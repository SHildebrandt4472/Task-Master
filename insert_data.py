from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from setup_db import User, ToDo

# Connect to the database
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
session = Session()

# Insert users with hashed passwords
user1 = User(username='sam',
             password=generate_password_hash('password123'),
             display_name='Sam the boss')

user2 = User(username='jane_doe',
             password=generate_password_hash('mypassword'),
             display_name='Jane Doe')

user3 = User(username='john_doe',
             password=generate_password_hash('password'),
             display_name='John Doe')


session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

# Insert tasks
task1 = ToDo(task='Learn SQLAlchemy', done=False, user_id=user1.id)
task2 = ToDo(task='Build an app', done=False, user_id=user2.id)
task3 = ToDo(task='Buy groceries', done=True, user_id=user3.id)
task4 = ToDo(task='Do laundry', done=False, user_id=user1.id)
task5 = ToDo(task='Cook dinner', done=True, user_id=user2.id)

session.add(task1)
session.add(task2)
session.add(task3)
session.add(task4)
session.add(task5)
session.commit()

print("Users and tasks inserted successfully.")