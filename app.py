import os, os.path
import cherrypy
from jinja2 import Environment, FileSystemLoader

# Package level imports
from CherryBlog import main, admin, register

if __name__ == '__main__':

	front = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
	}

	secure = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
			'tools.auth_basic.on': True,
			'tools.auth_basic.realm': 'CherryBlog',
			'tools.auth_basic.checkpassword': admin.AdminPages.login
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
	}

	# Setup template engine and start server
	env = Environment(loader=FileSystemLoader('templates'))

	cherrypy.tree.mount(admin.AdminPages(env), '/admin', secure)
	cherrypy.tree.mount(register.RegisterPages(env), '/setup', front)
	cherrypy.quickstart(main.MainPages(env), '/', front)