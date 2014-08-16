import cherrypy
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
		# If no username or password is set on first login
		# prompt the user to set one for the account.
		if admin.AdminModel.userExists() == True:
			return self.firstLogin()

		return self.render("admin.html")

	@cherrypy.expose
	def firstLogin(self):
		return self.render("setup.html")