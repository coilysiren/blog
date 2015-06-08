#builtin scripts
import glob
#external scripts
import yaml
import sass
import flask
from flask_misaka import Misaka
#custom scripts
from cms import Cms

app = flask.Flask(__name__, static_folder='static', static_url_path='')

SITENAME = "Lynn Blog"
AVATAR = "http://www.gravatar.com/avatar/b1cde28ce033c8cd6f4be4059efbe00b.png?size=160"
URL = "http://lynncyrin.me"
DESC = "The blog of a Queer, Feminist, Programmer - Lynn Cyrin"

app.config.from_object(__name__)

cms = Cms(app)
Misaka(app)

# @app.before_request
def _before_request(self):
    if not flask.request.endpoint in ['']:
        print(flask.request.method+' '+str(flask.request.path)+' endpoint '+str(flask.request.endpoint)+'()')

@app.template_filter("snippet")
def snippet(post_content):
    for seperator in ('<readmore/>', '<br>', '<br/>', '</p>'):
        if seperator in post_content:
            break
    return flask.Markup(post_content.split(seperator, 1)[0])

#index page
@app.route('/index')
@app.route('/')
def index ():
    return flask.render_template('base.jade',
        posts = [
            'posts/origin-story.md',
            'posts/intern-problems.md',
            'posts/health-tracker.md',
            'pages/about.md'
        ]
    )

#about page
@app.route('/about')
def about ():
    return flask.render_template(
        'post.jade',
        page_title=app.config['SITENAME']+' // About Me',
        page_desc=app.config['DESC']+' // Information about me',
        posts=['pages/about.md', 'pages/contact.md']
    )

#contact page
@app.route('/contact')
def contact ():
    return flask.render_template(
        'post.jade',
        page_title=app.config['SITENAME']+' // Contact',
        page_desc=app.config['DESC']+' // Contact information and links',
        posts=['pages/contact.md'])

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
        with open('templates/posts/'+post_title+'.md') as f:
            post = f.read()
    except IOError:
        return page_not_found(404)

    meta = cms.get_metadata(post, post_title)

    return flask.render_template('post.jade',
        page_title=app.config['SITENAME']+' // '+meta['title'],
        page_desc=meta['desc'],
        posts=['posts/'+post_title+'.md'])

@app.route('/static/<path:filename>')
def base_static(filename):
    return flask.send_from_directory(app.root_path + '/static/', filename)

@app.route('/tagged/<tag>')
def tagged_page (tag):
    posts = list()
    for post_path in glob.glob('templates/posts/*'):
        with open(post_path) as f:
            post_content = f.read()
        meta = cms.get_metadata(post_content, post_path)
        if tag in meta['tags']:
            posts.append(post_content)
    return flask.render_template('base.jade',
        page_title=app.config['SITENAME']+' // '+tag,
        page_desc='Posts tagged '+tag,
        posts=posts)

@app.errorhandler(404)
def page_not_found (e):
    return flask.render_template('post.jade',
        page_title=app.config['SITENAME']+' // Error 404',
        page_desc='Page Not Found',
        posts=['pages/404.md'])


#debug mode start options


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
