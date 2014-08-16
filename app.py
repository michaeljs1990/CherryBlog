import os, os.path
import cherrypy
from jinja2 import Environment, FileSystemLoader

# Package level imports
from CherryBlog import main, admin

if __name__ == '__main__':

	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
	}

	# Setup template engine and start server
	env = Environment(loader=FileSystemLoader('templates'))

	cherrypy.tree.mount(admin.AdminPages(env), '/admin', conf)
	cherrypy.quickstart(main.MainPages(env), '/', conf)