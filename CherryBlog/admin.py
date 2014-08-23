import cherrypy
import cgi, os
import cgitb;

from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid, Invalid
from jinja2 import Environment, FileSystemLoader

# Import needed models
from CherryBlog.models import admin, blog

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
		return self.render("admin/admin.html")

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
		picture = admin.AdminModel().getKey("about_picture")

		return self.render("admin/settings.html", site_title=title, about_picture=picture)

	# Upload a picture to /public/uploads
	@cherrypy.expose
	def upload(self, **kwargs):
		form_data = cherrypy.request.body.params;

		# Upload file to folder.
		try:
			cgitb.enable()
			form = cgi.FieldStorage()
			form = form_data['upload']
			print(form)
			if form.filename:
				# strip leading path from file name to avoid directory traversal attacks
				fn = os.path.basename(form.filename)
				open('public/uploads/' + fn, 'wb').write(form.file.read())
		except Exception as err:
			print(err)

		# Key was changed successfully
		raise cherrypy.HTTPRedirect("/admin/settings")

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
			return self.render("admin/settings.html", error=str(err))

		# Key was changed successfully
		raise cherrypy.HTTPRedirect("/admin/settings")

	@cherrypy.expose
	def pages(self):
		return self.render("admin/pages.html")

	# All Blog handling functions below
	# Blog returns all blog posts and displays
	# button for the user to create a new one.
	@cherrypy.expose
	def blog(self):
		# post, tags, and released returned form the db
		posts = blog.BlogModel().getAll().fetchall();

		return self.render("admin/blog.html", posts=posts)

	# Display the new blog page. Nothing else is
	# needed to be handled on this page.
	# This also handles cases where a blog
	# is being edited when slug is passed in.
	@cherrypy.expose
	def newblog(self, bid=None):
		# If id is set we need to load in some data
		if bid != None:
			data = blog.BlogModel().editBlog(bid)

		tmpl = self._env.get_template("admin/newblog.html")

		if bid is None:
			return tmpl.render()
		else:
			return tmpl.render(data=data)

	# Add a new blog post into the database.
	# Nothing is returned from this method.
	@cherrypy.expose
	@cherrypy.tools.json_in()
	def blogPost(self, **kwargs):
		json = cherrypy.request.json

		validation = Schema({
			Required('post'): All(str, Length(max=250)),
			Required('content'): str,
			Required('released'): str,
			'tags': All(str, Length(max=2000)),
		})

		slug = json['post'].strip().replace (" ", "-")

		try:
			validation(json)
			if not blog.BlogModel().newBlog(json['post'].strip(), slug, json['tags'].strip(), json['released'].strip(), json['content'].strip()):
				raise cherrypy.HTTPError(406)
		except Exception as err:
			raise cherrypy.HTTPError(400)

	# Add a new blog post into the database.
	# Nothing is returned from this method.
	@cherrypy.expose
	@cherrypy.tools.json_in()
	def blogPut(self, bid, **kwargs):
		json = cherrypy.request.json

		validation = Schema({
			Required('post'): All(str, Length(max=250)),
			Required('content'): str,
			Required('released'): str,
			'tags': All(str, Length(max=2000)),
		})

		slug = json['post'].strip().replace (" ", "-")

		try:
			validation(json)
			if not blog.BlogModel().updateBlog(json['post'].strip(), slug, json['tags'].strip(), json['released'].strip(), json['content'].strip(), bid):
				raise cherrypy.HTTPError(406)
		except Exception as err:
			raise cherrypy.HTTPError(400)