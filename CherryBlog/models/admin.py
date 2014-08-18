import sqlite3
import hashlib
import binascii

class AdminModel(object):

	@classmethod
	def connector(cls):
		return sqlite3.connect('CherryBlog/models/app.db')

	# Check for the existence of a user in the database
	# return @bool
	@staticmethod
	def userExists():
		db = AdminModel.connector()
		cursor = db.execute('''SELECT COUNT(*) FROM users;''')
		
		if cursor.fetchone()[0] == 0:
			return False;
		else:
			return True

	# Add new user to the database
	@staticmethod
	def addUser(username, password):
		db = AdminModel.connector()

		uname = username.encode('utf-8')

		# Secure Hashing for the password
		passwd = AdminModel.computeHash(password)

		cursor = db.execute('''INSERT INTO users(username, password) VALUES (?, ?);''', (uname, passwd))
		
		try:
			db.commit()
			return True
		except Exception as err:
			return False

	@staticmethod
	def getUser(username):
		db = AdminModel.connector()
		cursor = db.execute('''SELECT * FROM users WHERE username=?;''', (username.encode('utf-8'),))
		return cursor


	@staticmethod
	def computeHash(password, salt="magicpy"):
		dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
		return binascii.hexlify(dk)