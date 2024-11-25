


if not defined VIRTUAL_ENV (
  call venv\scripts\activate.bat
)

set FLASK_APP=todo.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --debug
