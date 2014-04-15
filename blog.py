'''
__NAME__ = blog.py
__DESC__ = Routing and content generation file
__SIGN__ = Lynn Cyrin

Use:
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


#views


@app.route('/index')
@app.route('/home')
@app.route('/')
def index (): 
    #TODO: index should return about + 3 most recent posts
    print('loading /index')
    return flask.render_template('post.html', post_urls=['pages/about.html'])

@app.route('/about')
@app.route('/aboutme')
@app.route('/me')
def about ():
    print('loading /about') 
    return flask.render_template('post.html', post_urls=['pages/about.html'])

@app.route('/contact')
@app.route('/email')
@app.route('/twitter')
@app.route('/facebook')
@app.route('/skype')
def contact ():
    #need to put contact info on all pages also
    print('loading /contact') 
    return flask.render_template('post.html', post_urls=[PAGE_DIR+'contact.html'])

@app.route('/name')
@app.route('/cyrin')
@app.route('/conway')
def name ():
    print('loading /name') 
    return flask.render_template('post.html', post_urls=[PAGE_DIR+'name.html'])

@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
@app.route('/work')
def professional ():
    print('loading /work') 
    return flask.render_template('post.html', post_urls=[PAGE_DIR+'resume.html', PAGE_DIR+'projects.html', PAGE_DIR+'html.html'])

@app.errorhandler(404)
def page_not_found (e):
    print('page not found') 
    return flask.render_template('post.html', post_urls=[PAGE_DIR+'404.html']), 404

@app.route('/post/<post_title>')
@app.route('/posts/<post_title>')
def show_post_by_title (post_title):
    post_title = post_title.lower() #clean input
    if app.config['DEBUG']: build_post(post_title) #build your html file
    try:
        with open('templates/posts/'+post_title+'.html'): pass
    except IOError: return page_not_found(404)
    print('loading '+post_title)
    return flask.render_template('post.html', post_urls=['templates/posts/'+post_title+'.html'])

@app.route('/recent/<post_number>')
def show_post_by_recentness (post_number):
    return "WIP"


#functions


def refresh_content ():
    '''
    makes html from markdown post files
    starting a developement server rebuilds all articles
    '''
    #get content
    posts = glob.glob('posts/*')
    pages = glob.glob('pages/*')
    content = list()
    #combine pages + posts
    for article in posts:
        content.append(article)
    for article in pages:
        content.append(article)
    #remove previous html
    all_built = glob.glob('templates/posts/*')
    for post in all_built: os.remove(post)
    all_built = glob.glob('templates/pages/*')
    for post in all_built: os.remove(post)
    #create new html
    for article in content:
        html = 'templates/'+article[:-3]+'.html' #clip '.md'
        markdown.markdownFromFile(input=article, output=html)
        print('creating article '+article) 

def build_post (build):
    '''
    makes html from markdown post files
    rebuilds the post with every request (in debug mode)

    input: 'postname' ([not] post/postname.md)
    '''
    #check input
    if type(build) == str: build = [build] 
    try:
        for post in build:
            with open('posts/'+post+'.md'): pass #does this post exist?
        posts = build
    except IOError: 
        print('[build_html('+str(build)+')] invalid build input')
        return 0
    #create new posts
    for post in posts:
        md = 'posts/'+post+'.md'
        html = 'templates/posts/'+post+'.html'
        markdown.markdownFromFile(input=md, output=html)
        print('created post '+post) 

if __name__ == '__main__':
    print('staring in DEBUG mode...')
    app.config['DEBUG'] = True
    refresh_content()
    flask.ext.scss.Scss(app)
    app.run()