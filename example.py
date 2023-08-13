import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("data.db")
cursor =  connection.cursor()

# Query all data based on a condition
cursor.execute("SELECT * FROM events WHERE date='2008.10.10'")
rows = cursor.fetchall()
print(rows)

# Query certain columns based on a condition
cursor.execute("SELECT band,date FROM events WHERE date='2008.10.10'")
rows = cursor.fetchall()
print(rows)

# Insert new rows
# new_rows = [('Cat', 'Cat city', '2008.10.17'),
#             ('Hens', 'Hens city', '2008.10.10')]
#
#
# #"INSERT INTO events VALUES('Tigers', 'Tiger city', '2008.10.10')"
#
# cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
# connection.commit()

# Query all data
cursor.execute("SELECT band,date FROM events ")
rows = cursor.fetchall()
print(rows)

