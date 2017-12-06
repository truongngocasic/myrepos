activate_this = '/var/www/env_generator/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os
import sys
 
sys.path.append('/var/www/env_generator')

basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['FLASK_CONFIG'] = 'production'
os.environ['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../dbase/app.db')
 
from run import app as application
