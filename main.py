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
#custom scripts
import cms

app = flask.Flask(__name__, static_folder='static', static_url_path='')
app.config = {
    "SITENAME": "Lynn Blog",
    "AVATAR": "http://www.gravatar.com/avatar/b1cde28ce033c8cd6f4be4059efbe00b.png?size=160",
    "URL": "http://lynncyrin.me",
    "DESC": "The blog of a Queer, Feminist, Programmer - Lynn Cyrin",
}

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
        post_urls=['pages/contact.html', 'pages/gamer_tags.html', 'pages/contact_guide.html',])

@app.route('/resume')
def resume():
    return flask.send_from_directory(app.root_path + '/resume/', 'resume.html')

@app.route('/resume.pdf')
def resume_pdf():
    return flask.send_from_directory(app.root_path + '/resume/', 'resume.pdf')

@app.route('/resume.css')
def resume_css():
    return flask.send_from_directory(app.root_path + '/resume/', 'resume.css')

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

@app.route('/static/main.scss')
def render_css():
    return sass.compile(filename='static/main.scss', output_style='compressed')

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
    app.run()
