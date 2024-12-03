from flask import render_template, flash, redirect, url_for, request, abort, session
from .main_forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app.models import db, User, Task
from app.main import bp
import datetime
from sqlalchemy import text


@bp.route('/')
@bp.route('/index')
def home():
    if not current_user.is_authenticated:
      return redirect(url_for('.login'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(text('due_by is null, due_by')).all()
    overdue_tasks = []
    upcoming_tasks = []
    important_tasks = []
    recently_added_tasks = []
    for task in tasks:
      if task.is_overdue():
        overdue_tasks.append(task)
      elif task.is_important() and task.is_outstanding():
        important_tasks.append(task)  
      elif task.is_coming_up():
        upcoming_tasks.append(task)      
      elif task.is_recently_added() and task.is_outstanding():
        recently_added_tasks.append(task)

    session['back_to'] = request.path # Store the current url to come back to    
    return render_template('index.html', 
                              title='Home',
                            upcoming_tasks=upcoming_tasks, 
                            overdue_tasks=overdue_tasks, 
                            important_tasks=important_tasks, 
                            recently_added_tasks=recently_added_tasks) 

@bp.route('/categorytasks/<category>')
@login_required
def category_tasks(category):

    if category == 'All':
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(text('due_by is null, due_by')).all()
    elif category == 'Other':
        tasks = Task.query.filter_by(user_id=current_user.id, category='').order_by(text('due_by is null, due_by')).all()
    else:
      tasks = Task.query.filter_by(user_id=current_user.id, category=category).order_by(text('due_by is null, due_by')).all()

    categories_rows = Task.query.with_entities(Task.category).filter_by(user_id=current_user.id).distinct()
    categories = [row[0] for row in categories_rows]
    for cat in categories:
      if not cat:
        categories.remove(cat)
        categories.append('Other')
    categories = ['All'] + categories

    session['back_to'] = request.path # Store the current url to come back to    
    return render_template('category_tasks.html', tasks=tasks, categories=categories, selected_category=category)
   

@bp.route('/new')
@bp.route('/new/<category>')
@login_required
def new_task(category=None):
  task = Task()
  if category != "All" and category != "Other":
    task.category = category
  return render_template('new_task.html', 
                         task=task, 
                         action_url = url_for('main.add_task', id=task.id),
                         back_to_url = session['back_to'])

@bp.route('/add>', methods=['POST'])
@login_required
def add_task():
    task = Task()
    task.name = request.form['name']
    task.description = request.form['description']
    task.category = request.form['category'].title()    
    task.priority = request.form['priority']
    if request.form['due_by']:
      task.due_by = datetime.datetime.strptime(request.form['due_by'], '%Y-%m-%d')

    current_user.tasks.append(task) # add the task to the users list of tasks
    db.session.commit()             # store the data in the data base file

    return redirect(session['back_to'] or url_for('.home'))
                    

@bp.route('/edit/<id>')
@login_required
def edit_task(id):
    task = Task.query.get(id)
    if not task or task.user_id != current_user.id:       
      abort(403)
       
    return render_template('edit_task.html', 
                           task=task, 
                           action_url = url_for('main.update_task', id=task.id),
                           back_to_url = session['back_to'])
    
@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_task(id):
    task = Task.query.get(id)
    if not task or task.user_id != current_user.id:       
      abort(403)

    task.name = request.form['name']
    task.description = request.form['description']
    task.category = request.form['category'].title()
    task.priority = request.form['priority']
    if request.form['due_by']:
      task.due_by = datetime.datetime.strptime(request.form['due_by'], '%Y-%m-%d') 
    db.session.commit() 
    return redirect(session['back_to'] or url_for('.home'))    

@bp.route('/complete/<id>', methods=['POST'])
@login_required
def complete_task(id):
    task = Task.query.get(id)    
    if not task or task.user_id != current_user.id:       
      abort(403)

    task.done()
    db.session.commit()    
    return redirect(session['back_to'] or url_for('.home'))

@bp.route('/uncomplete/<id>', methods=['POST'])
@login_required
def uncomplete_task(id):
    task = Task.query.get(id)    
    if not task or task.user_id != current_user.id:       
      abort(403)

    task.undo()
    db.session.commit()
    return redirect(session['back_to'] or url_for('.home'))

@bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get(id)    
    if not task or task.user_id != current_user.id:       
      abort(403)

    db.session.delete(task)
    db.session.commit()
    return redirect(session['back_to'] or url_for('.home'))


## -- Login and Register routes --------------

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
