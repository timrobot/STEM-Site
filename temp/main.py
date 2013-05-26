#!usr/bin/env python

import os, cgi
import webapp2, jinja2
import searchEngine

from google.appengine.ext import ndb

jenv = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ["jinja2.ext.autoescape"])

def get_meta_content( page, meta ):
	location = page.find("meta")
	while location != -1:
		endtag = page.find(">", location)
		name = page.find("name", location)
		name = page.find("\"", name) + 1
		if name < endtag:
			if page[name:page.find("\"", name)] == meta:
				content = page.find("content", location)
				content = page.find("\"", content) + 1
				if content < endtag:
					return page[content:page.find("\"", content)]
		location = page.find("meta", endtag)
	return ""

def defaultColor():
    return "black"

def getColor(page):
	color = get_meta_content(page, "color")
	if (color == ""):
		color = defaultColor()
	return color

def getTemplateUrl(page):
	template = get_meta_content(page, "template")
	if (template == ""):
		template = "template.html"
	return template

def reformat(template):
	color = getColor(template)
	url = getTemplateUrl(template)
	if (url.lower() != "none"):
		return jenv.get_template(url).render({"color": color, "code": template})
	else:
		return template

class home(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("home.html")
		self.response.write(reformat(template.render({})))

class redirectHome(webapp2.RequestHandler):
	def get(self):
		self.redirect("/")

class biology(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("biology.html")
		self.response.write(reformat(template.render({})))

class chemistry(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("chemistry.html")
		self.response.write(reformat(template.render({})))

class physics(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("physics.html")
		self.response.write(reformat(template.render({})))

class medicine(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("medicine.html")
		self.response.write(reformat(template.render({})))

class mathematics(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("mathematics.html")
		self.response.write(reformat(template.render({})))

class robotics(webapp2.RequestHandler):
	def get(self):
		template = jenv.get_template("robotics.html")
		self.response.write(reformat(template.render({})))

class searchpage(webapp2.RequestHandler):
	def post(self):
		query = self.request.get("query")
		engine = searchEngine.Engine()
		engine.jinja_environment = jenv
		index = engine.search_web(query)
		results = []
		i = 0
		for result in index:
			results.append({
				"name": result.name,
				"icon": result.icon,
				"description": result.description,
				"url": result.url,
				"number": i
				})
			i += 1

		template = jenv.get_template("search.html")
		self.response.write(reformat(
			template.render({"results": results})
			))

app = webapp2.WSGIApplication([
		("/", home),
		("/home.html", redirectHome),
		("/biology.html", biology),
		("/chemistry.html", chemistry),
		("/physics.html", physics),
		("/medicine.html", medicine),
		("/mathematics.html", mathematics),
		("/robotics.html", robotics),
		("/search.html", searchpage)
	], debug = True)
