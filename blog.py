#blog.py

import os
import flask
import yaml
import markdown
import flask.ext.scss

#start app and set configuration
app = flask.Flask(__name__)
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
	app.config[key] = value
flask.ext.scss.Scss(app)


#views

@app.route('/')
@app.route('/home')
@app.route('/index')
def index (): 
	#TODO: index should return about + 3 most recent posts
	return flask.render_template('post.html', post_urls=['pages/about.html'])

@app.route('/about')
def about (): return flask.render_template('post.html', post_urls=['pages/about.html'])

@app.route('/contact')
def contact (): return flask.render_template('post.html', post_urls=['pages/contact.html'])

@app.route('/name')
def name (): return flask.render_template('post.html', post_urls=['pages/name.html'])

@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
def professional (): return flask.render_template('post.html', post_urls=['pages/resume.html', 'pages/projects.html', 'pages/html.html'])

@app.errorhandler(404)
def page_not_found (e): return flask.render_template('post.html', post_urls=['pages/404.html']), 404

@app.route('/post/<post_title>')
def show_post_by_title (post_title):
	post_title = post_title.lower() #clean input
	file_built = build_html(post_title) #build your html file
	if file_built: post_url = 'rendered_posts/'+str(post_title)+'.html'
	else: return page_not_found(404) #no such file exists
	return flask.render_template('post.html', post_urls=[post_url])

@app.route('/recent/<post_number>')
def show_post_by_recentness (post_number):
	return "WIP"

#functions

def build_html (post_title):
	'''makes html from markdown files, or returns 0 if it cant'''
	html = 'templates/rendered_posts/'+str(post_title)+'.html'
	md = 'posts/'+str(post_title)+'.md'
	try: #look for an already created html file
		with open(html): pass; return 1
	#if none
	except IOError: 
		#look for a markdown file to turn into html
		try: markdown.markdownFromFile(input=md, output=html); return 1
		#if no markdown file then 'fail'
		except IOError: return 0 

#can be run via foreman
#or by running the python file directly:
if __name__ == '__main__':
	app.run()