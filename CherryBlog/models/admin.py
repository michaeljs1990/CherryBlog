import sqlite3

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
			return True;
		else:
			return False