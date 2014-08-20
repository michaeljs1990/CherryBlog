import sqlite3
import hashlib
import binascii

class AdminModel(object):

	def __init__(self):
		self._db = sqlite3.connect('CherryBlog/models/app.db')

	# Check for the existence of a user in the database
	# return @bool
	def userExists(self):
		cursor = self._db.execute('''SELECT COUNT(*) FROM users;''')
		
		if cursor.fetchone()[0] == 0:
			return False;
		else:
			return True

	# Add new user to the database
	def addUser(self, username, password):
		# Secure Hashing for the password
		passwd = AdminModel.computeHash(password)

		cursor = self._db.execute("INSERT INTO users(username, password) VALUES (?, ?);", (username, passwd))
		
		try:
			self._db.commit()
			return True
		except Exception as err:
			return False

	# Return an array of username and hashed password
	def getUser(self, username):
		cursor = self._db.execute("SELECT * FROM users WHERE username=?;", (username,))
		return cursor

	@staticmethod
	def computeHash(password, salt="magicpy"):
		dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
		return binascii.hexlify(dk)

	# Return the value of a given key as listed
	# inside of the database.
	# Returns False on failed key lookup
	def getKey(self, key):
		cursor = self._db.execute("SELECT * FROM options WHERE key=?;", (key,))

		return cursor.fetchone()[1]

	def updateKey(self, key, value):
		cursor = self._db.execute("UPDATE options SET value=? WHERE key=?;", (value, key))

		try:
			self._db.commit()
			return True
		except Exception as err:
			return err

	# Add new blog post to the databse.
	def newBlog(self, post, slug, tags, released, content):
		cursor = self._db.execute("INSERT INTO blog(post, slug, tags, released, content) VALUES(?, ?, ?, ?, ?)", (post, slug, tags, released, content))
		
		try:
			self._db.commit()
			return True
		except Exception as err:
			return err