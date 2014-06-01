'''
__name__ = cms.py
__desc__ = Content generation and management script
__sign__ = Lynn Cyrin

Use:
import cms
run = cms.cms(config)
'''

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


class cms (object):
    '''creates and manages blog content'''

    def __init__ (self, config):
        cms.config = config
        #get content
        posts = glob.glob('posts/*')
        pages = glob.glob('pages/*')
        content = list()
        #combine pages + posts
        for article in posts:
            content.append(article)
        for article in pages:
            content.append(article)
        #remove previous html
        all_built = glob.glob('templates/posts/*')
        for post in all_built: os.remove(post)
        all_built = glob.glob('templates/pages/*')
        for post in all_built: os.remove(post)
        #create base html, metadata, snippet
        for article in content:
            self.build_post(article[:-3])
            self.create_snippet('templates/'+article[:-3]+'.html')
        #create rss.xml
        self.create_rss(content)

    def create_snippet (self, article):
        '''snips posts at <readmore>'''
        if not re.search("post", article): return 0 #only snip posts (i.e. not pages)
        snip_name = article[:-5]+'_snipped.html' #define snip name
        #get file
        with open(article, 'r') as base_file: 
            all_lines = base_file.readlines()
        #look for the first line with readmore
        readmore = 0
        for i, line in enumerate(all_lines):
            if re.search("readmore", line): readmore = i
        #snip if you found readmore
        if not readmore: return 0
        snippet = all_lines[:readmore]
        #Add in a link to actually go read more!!!
        url = article[16:-5] #cut the path and filetype
        link_to_more = '<h4><a href="http://lynncyrin.me/post/'+url+'">[ Read More! ]</a></h4>\n'
        snippet.append(link_to_more)
        #save yer snip
        with open(snip_name, 'w') as snippet_file: 
            snippet_file.writelines(snippet) 
        print("created snippet "+snip_name)

    def build_post (self, post):
        '''
        makes html from markdown post files
        rebuilds the post with every request (in debug mode)

        input: 'post/postname.md'
        '''
        md_path = post+'.md'
        html_path = 'templates/'+post+'.html'
        yaml_path = 'templates/'+post+'_meta.yaml'
        #get markdown
        with open(md_path, 'r') as md_data:
            text = md_data.read()
        #create html file
        md = markdown.Markdown(extensions = ['meta'])
        html_data = md.convert(text)
        with open(html_path, 'w') as html_file:
            html_file.write(html_data)
        print('created post '+post) 
        #pages don't get metadata
        if not re.search("post", post): return 0
        #de-unicode-ify the metadata
        meta = dict()
        for k, v_list in md.Meta.items(): 
            if len(v_list) == 1:
                meta[str(k)] = str(v_list[0])
            else:
                meta[str(k)] = list() 
                for v in v_list:
                    meta[str(k)].append(str(v))
        #create metadata file
        with open(yaml_path, 'w') as yaml_file:
            yaml.dump(meta, yaml_file)    
        print('created metadata '+yaml_path)     

    def create_rss (self, posts):
        #initalize feed
        rss = PyRSS2Gen.RSS2(
            title = cms.config['SITENAME'],
            link = cms.config['URL'],
            description = cms.config['DESC'],
            lastBuildDate = datetime.datetime.now(),
            items = [])
        #create content items
        for post_title in posts:
            #only add posts to rss feed
            if not re.search("post", post_title): continue
            #load post metadata into rss item
            meta = yaml.load(file('templates/'+post_title[:-3]+'_meta.yaml','r'))
            item = PyRSS2Gen.RSSItem(
               title = meta['title'],
               link = meta['link'],
               description = meta['desc'],
               guid = PyRSS2Gen.Guid(meta['link']),
               pubDate = datetime.datetime(2003, 9, 6, 21, 49))
            rss.items.append(item)
        #write to xml
        rss.write_xml(open("static/rss.xml", "w"))
        print('created xml rss.xml')