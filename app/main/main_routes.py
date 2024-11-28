from flask import render_template, flash, redirect, url_for, request, session
from .main_forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app.models import db, User, Task
from app.main import bp
import datetime


@bp.route('/')
@bp.route('/index')
def home():
    if not current_user.is_authenticated:
      return redirect(url_for('.login'))
        
    return render_template('index.html', title='Home')
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('.home'))

    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data.lower()).first()
      if user is None:  # try searching for email
        user = User.query.filter_by(email=form.username.data, email_verified=True).first()

      if user and not user.password_hash:  # has no password (i.e. has been reset by Admin)
        if form.username.data and user.username and form.password.data == user.email:  # allow email address as password
          login_user(user, remember=form.remember_me.data)      
          return redirect(url_for('.change_password'))

      if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password','error')
        return redirect(url_for('.login'))
    
      # Valid user
      login_user(user, remember=form.remember_me.data)      

      next_page = request.args.get('next')
      if not next_page or urlparse(next_page).netloc != '':
        next_page = url_for('.home')
      return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()    
    flash('You have successfully logged out')
    return redirect(url_for('.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
      reg_code = form.registration_code.data.upper()
      if reg_code != "SIGNMEUP":
        flash('Registration Code is not valid, contact your site administrator','error')
        return redirect(url_for('.register'))

      user = User(username = form.username.data.lower(),
                  email = form.email.data,
                  display_name = form.display_name.data)
      user.set_password(form.password.data)

      db.session.add(user)
      db.session.commit()
      flash('Your registration is complete, please login to continue')
      return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@bp.route('/new', methods=['GET'])
def new_task():
  task = Task()
  return render_template('new_task.html', task=task, action_url = url_for('main.add_task', id=task.id))

@bp.route('/add>', methods=['POST'])
def add_task():
    task = Task()
    task.name = request.form['name']
    task.description = request.form['description']
    task.category = request.form['category']
    if request.form['due_by']:
      task.due_by = datetime.datetime.strptime(request.form['due_by'], '%Y-%m-%d')
    current_user.tasks.append(task)
    db.session.commit() 
    return redirect(url_for('.home'))

@bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get(id)
    return render_template('edit_task.html', task=task, action_url = url_for('main.update_task', id=task.id))
    
@bp.route('/update/<id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    task.name = request.form['name']
    task.description = request.form['description']
    task.category = request.form['category']
    if request.form['due_by']:
      task.due_by = datetime.datetime.strptime(request.form['due_by'], '%Y-%m-%d')
 
    db.session.commit() 
    return redirect(url_for('.home'))

@bp.route('/completed/<id>', methods=['GET', 'POST'])
def complete_task(id):
    task = Task.query.get(id)
    task.done()
    db.session.commit()
    return redirect(url_for('.home'))

@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('.home'))

