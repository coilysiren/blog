# !/usr/bin/python
# -*- coding: UTF-8

#builtin
import os
import glob
import datetime
#external
import flask
import misaka
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
        app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
        flask_misaka.Misaka(app, autolink=True, lax_html=True)
        #
        if app.config['DEBUG']:
            # build css on changes
            from watchdog.events import FileSystemEventHandler
            class If_scss_changes (FileSystemEventHandler):
                def on_modified (self, event): Cms.build_css()

            # monitor for changes
            from watchdog.observers import Observer
            watch = Observer()
            watch.schedule(If_scss_changes(), os.path.dirname(__file__)+'/static/scss/')
            watch.start()

        # do a build
        Cms.build_css()

    @staticmethod
    def markdown(text):
        return misaka.html(text,
            extensions=misaka.EXT_LAX_HTML_BLOCKS | misaka.EXT_AUTOLINK)

    @staticmethod
    def snippet(text, path):
        for seperator in ('<readmore/>', '<br>', '<br/>', '</p>'):
            if seperator in text:
                break
        snip = text.split(seperator, 1)[0]
        url = '/posts/'+path.split('/')[-1].split('.')[0]
        snip += '<div class="readmore"><a href="{}" title="the post\'s not done! Here\'s the rest">Continued...</a></div>'.format(url)
        return snip

    @staticmethod
    def create_markdown_snippets(paths):
        posts = []
        for path in paths:
            if path[-3:] != '.md':
                path += '.md'
            if path[:10] == 'templates/':
                path = path[10:]
            with open('templates/'+path) as f:
                text = f.read()
            text = flask.Markup(Cms.snippet(Cms.markdown(text), path))
            posts.append(text)
        return posts

    @staticmethod
    def create_markdown(path):
        with open('templates/'+path+'.md') as f:
            text = f.read()
        return [flask.Markup(Cms.markdown(text))]

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
