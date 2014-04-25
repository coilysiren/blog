'''
__NAME__ = blog.py
__DESC__ = Routing and content generation file
__SIGN__ = Lynn Cyrin

Use:
[Production] '$ foreman start'
[Developement] '$ python blog.py' (runs in debug mode)
'''

import re
import os
import sys
import yaml
import glob
import flask
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
    post_urls = ['pages/landing.html', 'posts/countdowntoliftoff_snipped.html', 'posts/origin-story_snipped.html', 'posts/thebadvocatemag_snipped.html', 'pages/about.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/aboutme')
@app.route('/about')
def about ():
    page_title = app.config['SITENAME']+' // About Me'
    page_desc = app.config['DESC']+' // Information about me'
    post_urls = ['pages/about.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/contact')
def contact ():
    page_title = app.config['SITENAME']+' // Contact'
    page_desc = app.config['DESC']+' // Contact information and links'
    post_urls = ['pages/contact.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/cyrin')
@app.route('/conway')
@app.route('/name')
def name ():
    page_title = app.config['SITENAME']+' // Cyrin? Conway?'
    page_desc = app.config['DESC']+' // About my [last] name'
    post_urls = ['pages/name.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
@app.route('/work')
def professional ():
    page_title = app.config['SITENAME']+' // My Work'
    page_desc = app.config['DESC']+' // Work, projects, resume, etc...'
    post_urls = ['pages/resume.html', 'pages/projects.html', 'pages/experience.html', 'pages/html.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

@app.errorhandler(404)
def page_not_found (e):
    page_title = app.config['SITENAME']+' // Error 404'
    page_desc = 'Page Not Found'
    post_urls = ['pages/404.html']
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls), 404

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

@app.route('/posts')
def posts_page ():
    return "WIP"

@app.route('/tagged/<tag>')
def show_posts_by_tag (tag):
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
    base_html = list()
    for article in content:
        html = 'templates/'+article[:-3]+'.html' #clip '.md'
        markdown.markdownFromFile(input=article, output=html)
        base_html.append(html)
        print('creating article '+article[:-3]+'.html') 
    #create post snippets
    for base_name in base_html:
        #only snip posts (i.e. not pages)
        if not re.search("post", base_name): continue
        #define snip name
        snip_name = base_name[:-5]+'_snipped.html'
        #get file
        with open(base_name, 'r') as base_file: 
            all_lines = base_file.readlines()
        #look for the first line with readmore
        readmore = 0
        for i, line in enumerate(all_lines):
            if re.search("readmore", line): readmore = i
        #snip if you found readmore
        if not readmore: continue
        snippet = all_lines[:readmore]
        #Add in a link to actually go read more!!!
        url = base_name[16:-5] #cut the path and filetype
        link_to_more = '<h4><a href="http://lynncyrin.me/post/'+url+'">[ Read More! ]</a></h4>\n'
        snippet.append(link_to_more)
        #save yer snip
        with open(snip_name, 'w') as snippet_file: 
            snippet_file.writelines(snippet) 
        print("created snippet: "+snip_name)

def build_post (post):
    '''
    makes html from markdown post files
    rebuilds the post with every request (in debug mode)

    input: 'postname' (not post/postname.md)
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
    app.config['DEBUG'] = True
    refresh_content()
    flask.ext.scss.Scss(app)
    app.run()