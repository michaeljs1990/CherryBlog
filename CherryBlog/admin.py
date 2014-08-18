import cherrypy

from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid, Invalid
from jinja2 import Environment, FileSystemLoader

# Import needed models
from CherryBlog.models import admin

# Houses all top level pages
class AdminPages(object):

	def __init__(self, env):
		self._env = env

	# Render Page
	def render(self, page, **kwargs):
		menu = {"Settings":"/admin/settings", "Pages":"/admin/pages", "Blog":"/admin/blog"}
		
		keys = {"template":page, "menu":menu, "header": "Admin"}

		for key in kwargs:
			keys[key] = kwargs[key]

		tmpl = self._env.get_template('partials/body.html')
		return tmpl.render(keys)

	@cherrypy.expose
	def index(self):
		return self.render("admin.html")

	# Only called by the cherrypy framework when logging
	# in for the first time.
	@staticmethod
	def login(realm, username, password):
		row = admin.AdminModel.getUser(username)

		try:
			verify = row.fetchone()[1]
			if verify == admin.AdminModel.computeHash(password):
				return True
		except Exception as err:
			return False

	@cherrypy.expose
	def settings(self):
		pass

	@cherrypy.expose
	def pages(self):
		pass

	@cherrypy.expose
	def blog(self):
		pass