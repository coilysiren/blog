#blog.py

import os
import flask
import yaml
import markdown

#start app and set configuration
app = flask.Flask(__name__)
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
	app.config[key] = value


#views

@app.route('/')
@app.route('/home')
@app.route('/index')
def index (): 
	return flask.render_template('index.html')

@app.route('/post/<post_title>')
def show_post_by_title (post_title):
	post_title = post_title.lower() #clean input
	file_built = build_html(post_title) #build your html file
	if file_built: post_url = 'rendered_posts/'+str(post_title)+'.html'
	else: return flask.render_template('404.html'), 404 #no such file exists
	return flask.render_template('post.html', post_url=post_url)

@app.route('/recent/<post_number>')
def show_post_by_recentness (post_number):
	return "WIP"

@app.errorhandler(404)
def page_not_found (e):
	return flask.render_template('404.html'), 404

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