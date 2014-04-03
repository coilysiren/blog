#serve.py

import os
import sqlite3
import flask

#initialize app
app = flask.Flask(__name__)
app.config.from_object(__name__)

#set configuration
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'blog.db'),
    DEBUG = True,
    SECRET_KEY = 'developement key',
    USERNAME = 'admin',
    PASSWORD = 'pass'
    ))
#doesn't currently exist
app.config.from_envvar('BLOG_SETTINGS', silent=True) 

#views
@app.route('/')
def index ():
    return flask.render_template('index.html')

@app.route('/lynn')
def lynn ():
    return 'successful lynn test'

@app.route('/tagged/<tag_input>')
def show_posts_with_tag (tag_input):
    return flask.render_template('tagged.html', tag_input=tag_input)

@app.route('/post/<int:post_id>')
def show_post_by_id (post_id):
    return 'you asked for post #%d' % post_id

#can be run via foreman
#or by running the python file directly:
if __name__ == '__main__':
    app.run()