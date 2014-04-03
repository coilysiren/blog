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

#database shenanigans
def init_database ():
    with app.app_context():
        #create an application context
        database = get_database()
        with app.open_resource('schema.sql', mode='r') as f: #as file
            database.cursor().executescript(f.read())
        database.commit()

def connect_database ():
    #what is rv??? unsure
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_database ():
    '''
    opens a new database connection if there isn't one for the current
    application context

    flask.g = general application context variable
    '''
    #if you haven't gotten the database and attached it to the g
    if not hasattr(flask.g, 'sqlite_database'):
        #then connect to it
        flask.g.sqlite_database = connect_database()
    #and return it?
    return flask.g.sqlite_database

@app.teardown_appcontext
def close_database (error):
    '''turns off the database connection when we are done with it'''
    if hasattr (flask.g, 'sqlite_database'):
        flask.g.sqlite_database.close()

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