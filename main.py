'''
__name__ = blog.py
__desc__ = Routing and content generation file
__sign__ = Lynn Cyrin

Use:
[Production] '$ foreman start'
[Developement] '$ python blog.py' (runs in debug mode)
'''


#builtin scripts
import os
import glob
#external scripts
import yaml
import flask
import stripe
import flask.ext.scss
#custom scripts
import cms


#start app and set configuration


# stripe
stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']
# init app
app = flask.Flask(__name__, static_folder='static', static_url_path='')
# my configs
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
    post_urls = list()
    post_urls.append('pages/landing.html')
    post_urls.append('posts/origin-story_snipped.html')
    post_urls.append('posts/intern-problems_snipped.html')
    post_urls.append('posts/health-tracker_snipped.html')
    post_urls.append('pages/about.html')
    #dont edit return line
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)

#about page
@app.route('/aboutme')
@app.route('/about')
def about ():
    page_title = app.config['SITENAME']+' // About Me'
    page_desc = app.config['DESC']+' // Information about me'
    post_urls = ['pages/about.html', 'pages/contact.html', 'pages/name.html']
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

@app.route('/tagged/<tag>')
def tagged_page (tag):
    page_title = app.config['SITENAME']
    page_desc = app.config['DESC']
    post_urls = list()
    for post in glob.glob('posts/*'):
        meta = yaml.load(file('templates/'+post[:-3]+'_meta.yaml','r'))
        if tag in meta['tags']:
            post_urls.append((post[:-3]+"_snipped.html"))
    return flask.render_template('post.html', page_title=page_title, page_desc=page_desc, post_urls=post_urls)


#debug mode start options


if __name__ == '__main__':
    app.config['DEBUG'] = True
    create_cms = cms.cms(app.config)
    flask.ext.scss.Scss(app)
    app.run()
