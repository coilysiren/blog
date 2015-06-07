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
        # app.before_request(self._before_request)

        # content building
        self.create_rss(app.config)
        flask_misaka.Misaka(
            app,
            autolink=True,
            lax_html=True,
            )
        #
        from watchdog.observers import Observer
        watch = Observer()
        watch.schedule(If_scss_changes(), os.path.dirname(__file__)+'/static/')
        watch.start()

    def create_rss(self, config):
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
    def get_metadata(post, path):
        import yaml
        from bs4 import BeautifulSoup
        html = BeautifulSoup(post)

        # parse markdown file
        meta = dict()
        try:
            for span in html.find(attrs={'class':'metadata'}).findChildren():
                try:
                    span_content = str(span.contents[0])
                    meta_dictionary = yaml.load(span_content)
                except yaml.parser.ParseError, IndexError:
                    print(path+' contains a ParseError')
                else:
                    meta.update(meta_dictionary)
        except AttributeError:
            pass

        # fill in any holes
        meta['title'] = meta.get('title', '')
        meta['desc'] = meta.get('desc', '')
        meta['tags'] = meta.get('tags', '')

        return meta
