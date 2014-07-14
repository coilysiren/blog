'''
__name__ = blog.py
__desc__ = Routing and content generation file
__sign__ = Lynn Cyrin

Use:
[Production] '$ foreman start'
[Developement] '$ python blog.py' (runs in debug mode)
'''


#builtin scripts
import glob
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
@app.route('/')
def index ():
    return flask.render_template('post.html',
        page_title=app.config['SITENAME'],
        page_desc=app.config['DESC'],
        post_urls=['pages/landing.html',
            'posts/origin-story_snipped.html',
            'posts/intern-problems_snipped.html',
            'posts/health-tracker_snipped.html',
            'pages/about.html'])

#about page
@app.route('/about')
def about ():
    return flask.render_template('post.html',
        page_title=app.config['SITENAME']+' // About Me',
        page_desc=app.config['DESC']+' // Information about me',
        post_urls=['pages/about.html', 'pages/contact.html', 'pages/name.html'])

#contact page
@app.route('/contact')
def contact ():
    return flask.render_template('post.html',
        page_title=app.config['SITENAME']+' // Contact',
        page_desc=app.config['DESC']+' // Contact information and links',
        post_urls=['pages/contact_guide.html', 'pages/contact.html'])

@app.route('/posts/<post_title>')
@app.route('/post/<post_title>')
def show_post_by_title (post_title):
    post_title = post_title.lower() #clean input
    try:
        with open('templates/posts/'+post_title+'.html'): pass
    except IOError:
        return page_not_found(404)
    meta = yaml.load(file('templates/posts/'+post_title+'_meta.yaml','r'))
    return flask.render_template('post.html',
        page_title=app.config['SITENAME']+' // '+meta['title'],
        page_desc=meta['desc'],
        post_urls=['posts/'+post_title+'.html'])

@app.route('/static/<path:filename>')
def base_static(filename):
    return flask.send_from_directory(app.root_path + '/static/', filename)

@app.route('/tagged/<tag>')
def tagged_page (tag):
    post_urls = list()
    for post in glob.glob('posts/*'):
        meta = yaml.load(file('templates/'+post[:-3]+'_meta.yaml','r'))
        if tag in meta['tags']:
            post_urls.append((post[:-3]+"_snipped.html"))
    return flask.render_template('post.html',
        page_title=app.config['SITENAME']+' // '+tag,
        page_desc='Posts tagged '+tag,
        post_urls=post_urls)

@app.errorhandler(404)
def page_not_found (e):
    return flask.render_template('post.html',
        page_title=app.config['SITENAME']+' // Error 404',
        page_desc='Page Not Found',
        post_urls=['pages/404.html'])


#debug mode start options


if __name__ == '__main__':
    app.config['DEBUG'] = True
    create_cms = cms.cms(app.config)
    flask.ext.scss.Scss(app)
    app.run()
