import cherrypy
from jinja2 import Environment, FileSystemLoader

from CherryBlog.models import admin

# Houses all top level pages
class MainPages(object):

	def __init__(self, env):
		self._env = env

	# Render Page
	def render(self, page, **kwargs):
		menu = {"Home":"/"}

		# Get site header from the database
		header = admin.AdminModel().getKey('site_title')

		keys = {"template":page, "menu":menu, "header":header}

		for key in kwargs:
			keys[key] = kwargs[key]

		tmpl = self._env.get_template('partials/body.html')
		return tmpl.render(keys)

	@cherrypy.expose
	def index(self):
		return self.render("index.html")