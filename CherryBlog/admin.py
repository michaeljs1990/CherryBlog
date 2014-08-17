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
		# If no username or password is set on first login
		# prompt the user to set one for the account.
		if admin.AdminModel.userExists() == False:
			return self.render("setup.html")

		return self.render("admin.html")

	# This function will fire on the first login
	# and add the user to the database
	@cherrypy.expose
	def register(self, **kwargs):
		form_data = cherrypy.request.body.params;

		validation = Schema({
			Required('username'): All(str, Length(min=4)),
			Required('password'): All(str, Length(min=8))
		})

		try:
			validation(form_data)
			if (" " in form_data["username"]) == True:
				raise Invalid("Username must not contain any spaces.")
			if not admin.AdminModel.addUser(form_data["username"], form_data["password"]):
				raise Invalid("Unable to add the user to the database.")
		except Exception as err:
			return self.render("setup.html", error=str(err))

		# Setup was complete successfully
		return self.render("admin.html")