# !/usr/bin/python
# -*- coding: UTF-8

#builtin
import os
import glob
import datetime
#external
import flask
import PyRSS2Gen
import flask_misaka

from watchdog.events import FileSystemEventHandler
class If_scss_changes (FileSystemEventHandler):
    def on_modified (self, event): Cms.build_css()

class Cms (object):

    def __init__ (self, app):

        # logging
        app.before_request(self._before_request)

        # content building
        self.create_rss(app.config)
        app.template_filter(Cms.snippet)
        flask_misaka.Misaka(app)
        #
        from watchdog.observers import Observer
        watch = Observer()
        watch.schedule(If_scss_changes(), os.path.dirname(__file__)+'/static/')
        watch.start()

    def _before_request(self):
        if not flask.request.endpoint in ['']:
            print(flask.request.method+' '+str(flask.request.path)+' endpoint '+str(flask.request.endpoint)+'()')

    def create_rss (self, config):
        last_modified = os.path.getmtime(max(glob.iglob('templates/posts/*'), key=os.path.getmtime))
        last_modified_datetime = datetime.datetime.fromtimestamp(last_modified)

        #initalize feed
        rss = PyRSS2Gen.RSS2(
            title = config['SITENAME'],
            link = config['URL'],
            description = config['DESC'],
            lastBuildDate = last_modified_datetime,
            items = [])

        # create content items
        posts = []
        for post_title in posts:
            meta = {}
            item = PyRSS2Gen.RSSItem(
               title = meta.get('title'),
               link = meta.get('link'),
               description = meta.get('desc'),
               guid = PyRSS2Gen.Guid(meta.get('link')),
               pubDate = last_modified_datetime
            )
            rss.items.append(item)

        #write to xml
        with open("static/rss.xml", "w") as f:
            rss.write_xml(f)

    @staticmethod
    def build_css():
        import sass
        with open(os.path.dirname(__file__)+'/static/css/main.css', 'w') as f:
            f.write(sass.compile(
                filename=os.path.dirname(__file__)+'/static/scss/main.scss',
                output_style='compressed',
                include_paths=os.path.dirname(__file__)+'/static/',
            ))
        print(' * Built css')

    @staticmethod
    def snippet(post_content):
        for seperator in ('<readmore/>', '<br>', '<br/>', '</p>'):
            if seperator in post_content:
                break
        return flask.Markup(post_content.split(seperator))
