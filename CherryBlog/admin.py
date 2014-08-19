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
		row = admin.AdminModel().getUser(username)

		try:
			verify = row.fetchone()[1]
			if verify == admin.AdminModel.computeHash(password):
				return True
		except Exception as err:
			return False

	# Allow user to set random blog settings and turn flags on
	# and off such as site title and pages.
	@cherrypy.expose
	def settings(self):
		# Get the site title
		title = admin.AdminModel().getKey("site_title")

		return self.render("settings.html", site_title=title)

	# Update all Key Value pairs in the database.
	@cherrypy.expose
	def settingsPost(self, **kwargs):
		form_data = cherrypy.request.body.params;

		validation = Schema({
			Required('site_title'): All(str, Length(max=1000))
		})

		try:
			validation(form_data)
			if not admin.AdminModel().updateKey("site_title", form_data["site_title"]):
				raise Invalid("Unable to add the user to the database.")
		except Exception as err:
			return self.render("settings.html", error=str(err))

		# Key was changed successfully
		raise cherrypy.HTTPRedirect("/admin/settings")

	@cherrypy.expose
	def pages(self):
		pass

	@cherrypy.expose
	def blog(self):
		pass