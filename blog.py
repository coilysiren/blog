'''
blog.py

Main routing file!

[Production] '$ foreman start'
[Developement] '$ python blog.py' (runs in debug mode)
'''

import os
import sys
import glob
import flask
import yaml
import markdown
import flask.ext.scss

#start app and set configuration
app = flask.Flask(__name__)
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
    app.config[key] = value

PAGE_DIR = '../pages/'
POST_DIR = '../posts/'

#views

@app.route('/index')
@app.route('/home')
@app.route('/')
def index (): 
    #TODO: index should return about + 3 most recent posts
    return flask.render_template('post.html', post_urls=[PAGE_DIR+'about.html'])

@app.route('/about')
def about (): return flask.render_template('post.html', post_urls=[PAGE_DIR+'about.html'])

@app.route('/contact')
def contact (): return flask.render_template('post.html', post_urls=[PAGE_DIR+'contact.html'])

@app.route('/name')
def name (): return flask.render_template('post.html', post_urls=[PAGE_DIR+'name.html'])

@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
def professional (): return flask.render_template('post.html', post_urls=[PAGE_DIR+'resume.html', PAGE_DIR+'projects.html', PAGE_DIR+'html.html'])

@app.errorhandler(404)
def page_not_found (e): return flask.render_template('post.html', post_urls=[PAGE_DIR+'404.html']), 404

@app.route('/post/<post_title>')
def show_post_by_title (post_title):
    post_title = post_title.lower() #clean input
    file_built = build_html(post_title) #build your html file
    if file_built: post_url = 'rendered_posts/'+post_title+'.html'
    else: return page_not_found(404) #no such file exists
    return flask.render_template('post.html', post_urls=[post_url])

@app.route('/recent/<post_number>')
def show_post_by_recentness (post_number):
    return "WIP"

#functions

def build_posts (build=[]):
    '''
    makes html from markdown post files
    debug mode rebuilds the post with every request
    starting a developement server rebuilds all posts
    
    valid input: 
        ['posts/candy.md', 'posts/awesome.md'] #list of posts
        'all' #to build all posts

    returns 0 if something broke
    '''
    #check input
    if build == 'all': posts = glob.glob('posts/*') #get all posts
    elif build and type(build) == list: 
        try: #check that all inputs are valid
            for post_path in build:
                with open(post_path): pass
            posts = build #if everything ok!
        except IOError: return 0 #if not then fail
    else: print('[build_posts('+str(build)+')] invalid build input'); return 0
    #remove previous
    if build == 'all':
        all_built = glob.glob('static/posts/*')
        for post in all_built: os.remove(post)
    else:
        try:
            for post in posts: os.remove('static/'+post)
        except OSError: pass #post might not already exist
    #create new

    #html = 'static/post/'+str(post_title)+'.html'
    #md = 'posts/'+str(post_title)+'.md'
    try: #look for an already created html file
        # very hacky solution. debug mode automatically 
        # regenerates all the md -> html files
        # (ie. this forces an IOError for this try statement)
        try:
            os.remove(html)
            print(log+'regenerating post html')
        except OSError: print(log+'no previous html file')
        with open(html): pass; return 1
    #if none
    except IOError: 
        #look for a markdown file to turn into html
        try: markdown.markdownFromFile(input=md, output=html); print(log+'creating post'); return 1
        #if no markdown file then 'fail'
        except IOError: print(log+'no such post'); return 0
        
if __name__ == '__main__':
    app.config['DEBUG'] = True
    flask.ext.scss.Scss(app)
    app.run(host='0.0.0.0') #havent gotten the host thing working yet