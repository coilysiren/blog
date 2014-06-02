'''
__name__ = blog.py
__desc__ = Routing and content generation file
__sign__ = Lynn Cyrin

Use:
[Production] '$ foreman start'
[Developement] '$ python blog.py' (runs in debug mode)
'''

#external scripts
import yaml
import flask
import flask.ext.scss
#custom scripts
import cms


#start app and set configuration


app = flask.Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
    app.config[key] = value


#views


#index page
@app.route('/index')
@app.route('/home')
@app.route('/')
def index (): 
    #need to get rid of the page_title + page_desc repitition
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    #things to display on the landing page
    post_urls = ['pages/landing.html', 'posts/origin-story_snipped.html', 'pages/about.html']
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

#about page
@app.route('/aboutme')
@app.route('/about')
def about ():
    page_title = app.config['SITENAME']+' // About Me'
    page_desc = app.config['DESC']+' // Information about me'
    post_urls = ['pages/about.html', 'pages/contact.html']
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

#contact page
@app.route('/contact')
def contact ():
    page_title = app.config['SITENAME']+' // Contact'
    page_desc = app.config['DESC']+' // Contact information and links'
    post_urls = ['pages/contact_guide.html', 'pages/contact.html']
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

#about my name page
@app.route('/cyrin')
@app.route('/conway')
@app.route('/name')
def name ():
    page_title = app.config['SITENAME']+' // Cyrin? Conway?'
    page_desc = app.config['DESC']+' // About my [last] name'
    post_urls = ['pages/name.html']
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

#work page
@app.route('/professional')
@app.route('/projects')
@app.route('/resume')
@app.route('/work')
def professional ():
    page_title = app.config['SITENAME']+' // My Work'
    page_desc = app.config['DESC']+' // Work, projects, resume, etc...'
    #work content sections
    post_urls = ['pages/resume.html', 'pages/projects.html', 'pages/experience.html', 'pages/html.html']
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)


#[/PAGES]


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

@app.route('/static/<path:filename>') 
def base_static(filename): 
    return flask.send_from_directory(app.root_path + '/static/', filename)

@app.route('/posts')
def posts_page ():
    return "WIP"

@app.route('/tagged/<tag>')
def show_posts_by_tag (tag):
    return "WIP"


#debug mode start options


if __name__ == '__main__':
    app.config['DEBUG'] = True
    create_cms = cms.cms(app.config)
    flask.ext.scss.Scss(app)
    app.run()