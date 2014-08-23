import sqlite3

class BlogModel(object):

	def __init__(self):
		self._db = sqlite3.connect('CherryBlog/models/app.db')

		# Add new blog post to the databse.
	def newBlog(self, post, slug, tags, released, content):
		cursor = self._db.execute("INSERT INTO blog(post, slug, tags, released, content) VALUES(?, ?, ?, ?, ?)", (post, slug, tags, released, content))
		
		try:
			self._db.commit()
			return True
		except Exception as err:
			return err

	def updateBlog(self, post, slug, tags, released, content, bid):
		cursor = self._db.execute("UPDATE blog SET post = ?, slug = ?, tags = ?, released = ?, content = ? WHERE id=?", (post, slug, tags, released, content, bid))
		
		try:
			self._db.commit()
			return True
		except Exception as err:
			return err

	def editBlog(self, bid):
		cursor = self._db.execute("SELECT * FROM blog WHERE id=?", (bid,))

		return cursor.fetchone()

	# Render list of posts without content
	def getAll(self):
		cursor = self._db.execute("SELECT post, slug, tags, released, id FROM blog ORDER BY id  DESC;")

		return cursor