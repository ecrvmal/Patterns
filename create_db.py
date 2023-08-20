import sqlite3

con = sqlite3.connect('framework.sqlite')
cur = con.cursor()
with open('create_db.sql', mode='r') as f:
    sql_script = f.read()
cur.executescript(sql_script)
cur.close()
con.close()


