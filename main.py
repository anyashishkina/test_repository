import sqlite3

con = sqlite3.connect("server.db")

cur = con.cursor()

for value in cur.execute("SELECT * FROM testfinaltable"):
    print(value)
