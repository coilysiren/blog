# !/usr/bin/python
# -*- coding: UTF-8

#builtin scripts
import re
import os
import sys
import glob
import datetime
#external scripts
import yaml
import markdown
import PyRSS2Gen


class Cms (object):
    '''
    __name__ = cms.py
    __desc__ = creates and manages blog content
    __sign__ = Lynn Cyrin

    Usage:
    import cms
    run = cms.cms(config)

    this file deals with special characters!
    take a look at cms.cms.to_ascii
    '''

    def __init__ (self, app):
        self.create_rss(app.config)

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
