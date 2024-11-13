from flask import Flask, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from setup_db import User, engine, ToDo

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()
current_user = session.query(User).first()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():

    return render_template('login.html')
    @app.route('/login', methods=['POST'])



def tasks():
    return render_template('tasks.html', current_user=current_user)
    @app.route('/add_task')
    
def add_task():
    task = ToDo(task='Buy groceries', user_id=1)
    session.add(task)
    session.commit()
    return redirect(url_for('sam'))

@app.route('/debug')
def debug():
    users = session.query(User).all()
    return render_template('debug.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
    