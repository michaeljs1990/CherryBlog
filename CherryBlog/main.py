import cherrypy
from jinja2 import Environment, FileSystemLoader

# Houses all top level pages
class MainPages(object):

	def __init__(self, env):
		self._env = env

	# Render Page
	def render(self, page, **kwargs):
		menu = {"Home":"/", "Blog":"/blog", "GitHub":"/github", "Projects":"/projects", "About":"/about"}

		keys = {"template":page, "menu":menu, "header": "Michael Schuett"}

		for key in kwargs:
			keys[key] = kwargs[key]

		tmpl = self._env.get_template('partials/body.html')
		return tmpl.render(keys)

	@cherrypy.expose
	def index(self):
		return self.render("index.html")