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
import datetime
import PyRSS2Gen
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
    post_title = post_title.lower() #clean input
    try:
        with open('templates/posts/'+post_title+'.html'): pass
    except IOError: return page_not_found(404)
    meta = yaml.load(file('templates/posts/'+post_title+'_meta.yaml','r'))
    page_title = app.config['SITENAME']+' // '+meta['title']
    page_desc = meta['desc']
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
    #create base html, metadata, snippet
    for article in content:
        build_post(article[:-3])
        create_snippet('templates/'+article[:-3]+'.html')
    #create rss.xml
    create_rss(content)

def create_snippet (article):
    '''snips posts at <readmore>'''
    if not re.search("post", article): return 0 #only snip posts (i.e. not pages)
    snip_name = article[:-5]+'_snipped.html' #define snip name
    #get file
    with open(article, 'r') as base_file: 
        all_lines = base_file.readlines()
    #look for the first line with readmore
    readmore = 0
    for i, line in enumerate(all_lines):
        if re.search("readmore", line): readmore = i
    #snip if you found readmore
    if not readmore: return 0
    snippet = all_lines[:readmore]
    #Add in a link to actually go read more!!!
    url = article[16:-5] #cut the path and filetype
    link_to_more = '<h4><a href="http://lynncyrin.me/post/'+url+'">[ Read More! ]</a></h4>\n'
    snippet.append(link_to_more)
    #save yer snip
    with open(snip_name, 'w') as snippet_file: 
        snippet_file.writelines(snippet) 
    print("created snippet "+snip_name)

def build_post (post):
    '''
    makes html from markdown post files
    rebuilds the post with every request (in debug mode)

    input: 'post/postname.md'
    '''
    md_path = post+'.md'
    html_path = 'templates/'+post+'.html'
    yaml_path = 'templates/'+post+'_meta.yaml'
    #get markdown
    with open(md_path, 'r') as md_data:
        text = md_data.read()
    #create html file
    md = markdown.Markdown(extensions = ['meta'])
    html_data = md.convert(text)
    with open(html_path, 'w') as html_file:
        html_file.write(html_data)
    print('created post '+post) 
    #pages don't get metadata
    if not re.search("post", post): return 0
    #de-unicode-ify the metadata
    meta = dict()
    for k, v_list in md.Meta.items(): 
        if len(v_list) == 1:
            meta[str(k)] = str(v_list[0])
        else:
            meta[str(k)] = list() 
            for v in v_list:
                meta[str(k)].append(str(v))
    #create metadata file
    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(meta, yaml_file)    
    print('created metadata '+yaml_path)     

def create_rss (posts):
    #initalize feed
    rss = PyRSS2Gen.RSS2(
        title = app.config['SITENAME'],
        link = app.config['URL'],
        description = app.config['DESC'],
        lastBuildDate = datetime.datetime.now(),
        items = [])
    #create content items
    for post_title in posts:
        #only add posts to rss feed
        if not re.search("post", post_title): continue
        #load post metadata into rss item
        meta = yaml.load(file('templates/'+post_title[:-3]+'_meta.yaml','r'))
        item = PyRSS2Gen.RSSItem(
           title = meta['title'],
           link = meta['link'],
           description = meta['desc'],
           guid = PyRSS2Gen.Guid(meta['link']),
           pubDate = datetime.datetime(2003, 9, 6, 21, 49))
        rss.items.append(item)
    #write to xml
    rss.write_xml(open("rss.xml", "w"))
    print('created xml rss.xml')


#debug mode start options


if __name__ == '__main__':
    app.config['DEBUG'] = True
    refresh_content()
    flask.ext.scss.Scss(app)
    app.run()