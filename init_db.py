#Module to initialize a db named "database.db" which will store 
#post IDs, time_created, Title, and Post content

import sqlite3

connection = sqlite3.connect('database.db')

# Executing schema.sql script to initialize our db
with open('schema.sql') as f:
    connection.executescript(f.read())

# Prepopulating the database for developmental purposes

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()