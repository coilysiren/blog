#blog.py

import os
import flask
import yaml

#start app and set configuration
app = flask.Flask(__name__)
app.config.from_object(__name__)
for key, value in yaml.load(file('config.yaml','r')).items():
    app.config[key] = value

#views
@app.route('/')
def index ():
    #get all posts in post directory (???)
    posts = list()
    #posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    #sort by data
    #posts.sort(key=lambda item:item['date'], reverse=False)
    return flask.render_template('base.html', posts=posts)

@app.route('/tagged/<tag_input>')
def show_posts_with_tag (tag_input):
    #tag_input = tag_input.lower()
    #something to handle spaces in tags? I'm going to have to use them
    posts = list()
    posts = [p for p in flatpages]
    tagged_posts = list()
    #for post in posts
        #if tag_input in post.tags:
            #tagged_posts.append(post)
    return flask.render_template('tagged.html', tag_input=tag_input,
        tagged_posts=tagged_posts)

@app.route('/post/<post_title>')
def show_post_by_title (post_title):
    path = '{}/{}'.format(POST_DIR, post_title)
    #post = flatpages.get_or_404(path)
    return flask.render_template('post.html', post=post)

#can be run via foreman
#or by running the python file directly:
if __name__ == '__main__':
    app.run()