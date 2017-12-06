#!flask/bin/python

import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

db = SQLAlchemy(app)
db.create_all()
