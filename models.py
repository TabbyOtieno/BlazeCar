import os
from app import app
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

# load dotenv in the base root
# refers to application_top
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

database_connection = os.getenv("DATABASE_URI")

app.config['SQLALCHEMY_DATABASE_URI'] = database_connection
db = SQLAlchemy(app)
