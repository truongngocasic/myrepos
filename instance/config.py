import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'p9Bv<3Eid9%$i01'
#SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../dbase/app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
