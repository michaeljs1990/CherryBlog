import cherrypy
from jinja2 import Environment, FileSystemLoader

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

		self.firstLogin()

		return self.render("admin.html")

	@cherrypy.expose
	def firstLogin(self):
		