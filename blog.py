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


print('loading BLOG!!!')
app = flask.Flask(__name__)
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
    app.config[key] = value


#views


@app.route('/index')
@app.route('/home')
@app.route('/')
def index (): 
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    #TODO: index should return about + 3 most recent posts
    print('loading /index')
    post_urls = ['pages/landing.html', 'posts/countdowntoliftoff.html', 'posts/origin-story.html', 'pages/about.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/aboutme')
@app.route('/about')
def about ():
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    print('loading /about')
    post_urls = ['pages/about.html']
    page_title += ' // About Me'
    page_desc += ' // Information about me'
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/contact')
def contact ():
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    #need to put contact info on all pages also
    print('loading /contact')
    post_urls = ['pages/contact.html']
    page_title += ' // Contact'
    page_desc += ' // Contact information and links'
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/cyrin')
@app.route('/conway')
@app.route('/name')
def name ():
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    print('loading /name') 
    post_urls = ['pages/name.html']
    page_title += ' // Cyrin? Conway?'
    page_desc += ' // About my [last] name'
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
@app.route('/work')
def professional ():
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    print('loading /work') 
    post_urls = ['pages/resume.html', 'pages/projects.html', 'pages/experience.html', 'pages/html.html']
    page_title += ' // My Work'
    page_desc += ' // Work, projects, resume, etc...'
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.errorhandler(404)
def page_not_found (e):
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    print('page not found') 
    post_urls = ['pages/404.html']
    page_title += ' // 404'
    page_desc = 'Page Not Found'
    return flask.render_template('post.html', post_urls=post_urls), 404

@app.route('/posts/<post_title>')
@app.route('/post/<post_title>')
def show_post_by_title (post_title):
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    post_title = post_title.lower() #clean input
    if app.config['DEBUG']: build_post(post_title) #build your html file
    try:
        with open('templates/posts/'+post_title+'.html'): pass
    except IOError: return page_not_found(404)
    print('loading /posts/'+post_title)
    post_urls = ['posts/'+post_title+'.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/recent/<post_number>')
def show_post_by_recentness (post_number):
    return "WIP"


#functions


def refresh_content ():
    '''
    makes html from markdown files
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
        print('creating article '+article[:-3]+'.html') 

def build_post (post):
    '''
    makes html from markdown post files
    rebuilds the post with every request (in debug mode)

    input: 'postname' (not! post/postname.md)
    '''
    #check input
    try:
        with open('posts/'+post+'.md'): pass #does this post exist?
    except IOError:
        print('[build_html('+str(post)+')] invalid build input')
        return 0
    #create new post
    md = 'posts/'+post+'.md'
    html = 'templates/posts/'+post+'.html'
    markdown.markdownFromFile(input=md, output=html)
    print('created post '+post) 


#debug mode start options


if __name__ == '__main__':
    print('staring in DEBUG mode...')
    app.config['DEBUG'] = True
    app.config['URL'] = "http://0.0.0.0:5000/"
    refresh_content()
    flask.ext.scss.Scss(app)
    app.run()