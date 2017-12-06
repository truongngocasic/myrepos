import sqlite3
import json

db = sqlite3.connect('dbase/app.db')

# Get a cursor object
cursor = db.cursor()

#Show project
print "SHOW PROJECT"
cursor.execute("SELECT * FROM project")
 
rows = cursor.fetchall()
 
for row in rows:
    print row
    print json.dumps(row)

#Show users
print "SHOW USERS"
cursor.execute("SELECT * FROM users")
 
rows = cursor.fetchall()
 
for row in rows:
    print(row)
