

rem This script assumes virtual environment is already active i.e.
rem  venv\Script\activate

set FLASK_APP=todo.py
set FLASK_ENV=development
python -m flask run --host=0.0.0.0 --debug
