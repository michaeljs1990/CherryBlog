import sqlite3

if __name__ == "__main__":

	db = sqlite3.connect('CherryBlog/models/app.db')

	db.execute('''CREATE TABLE IF NOT EXISTS users
	       (username	VARCHAR(250)	PRIMARY KEY NOT NULL,
	       password	VARCHAR(64)	NOT NULL);''')

	db.execute('''CREATE TABLE IF NOT EXISTS pages
	       (id	INTEGER PRIMARY KEY AUTOINCREMENT,
	       	page	VARCHAR(250)	NOT NULL,
	       slug	VARCHAR(250)	NOT NULL,
	       parent VARCHAR(250) NOT NULL,
	       released BOOLEAN NOT NULL,
	       content TEXT);''')

	db.execute('''CREATE TABLE IF NOT EXISTS blog
	       (id	INTEGER PRIMARY KEY AUTOINCREMENT,
	       	post	VARCHAR(250)	NOT NULL,
	       slug	VARCHAR(250)	NOT NULL,
	       tags TEXT,
	       released BOOLEAN NOT NULL,
	       content TEXT);''')

	db.execute('''CREATE TABLE IF NOT EXISTS options
	       (key	VARCHAR(250)	PRIMARY KEY	NOT NULL,
	       value	TEXT);''')

	db.execute('''CREATE TABLE IF NOT EXISTS uploads
	       (name	VARCHAR(250)	PRIMARY KEY 	NOT NULL,
	       image	TEXT NOT NULL);''')

	# Insert default key value pairs
	db.execute('''INSERT INTO options(key, value) VALUES ("site_title", "CherryBlog");''')
	db.execute('''INSERT INTO options(key, value) VALUES ("about_picture", "cherrypy.png");''')

	db.commit()
	print("CherryBlog DB created successfully");
	db.close()